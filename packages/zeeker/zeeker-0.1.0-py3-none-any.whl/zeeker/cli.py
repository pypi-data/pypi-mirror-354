"""
Zeeker Database Customization Library

A Python library to help database developers create compliant customizations
for Zeeker databases following the three-pass asset system.
"""

import json
import os
import re
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
import boto3
from jinja2 import Environment, FileSystemLoader, Template
import click
import yaml


@dataclass
class ValidationResult:
    """Result of validation operations."""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)


@dataclass
class DatabaseCustomization:
    """Represents a complete database customization."""

    database_name: str
    base_path: Path
    templates: Dict[str, str] = field(default_factory=dict)
    static_files: Dict[str, bytes] = field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = None


class ZeekerValidator:
    """Validates Zeeker database customizations for compliance."""

    # Banned template names that would break core functionality
    BANNED_TEMPLATES = {
        "database.html",
        "table.html",
        "index.html",
        "query.html",
        "row.html",
        "error.html",
        "base.html",
    }

    # Required metadata fields for complete Datasette structure
    REQUIRED_METADATA_FIELDS = {"title", "description"}

    @staticmethod
    def sanitize_database_name(name: str) -> str:
        """Sanitize database name following Datasette conventions."""
        # Replace special characters and add MD5 hash if needed
        sanitized = re.sub(r"[^a-zA-Z0-9_-]", "-", name)
        if sanitized != name:
            hash_suffix = hashlib.md5(name.encode()).hexdigest()[:6]
            sanitized = f"{sanitized}-{hash_suffix}"
        return sanitized

    def validate_template_name(self, template_name: str, database_name: str) -> ValidationResult:
        """Validate that template name is safe and follows conventions."""
        result = ValidationResult(is_valid=True)

        # Check if template name is banned
        if template_name in self.BANNED_TEMPLATES:
            result.is_valid = False
            result.errors.append(
                f"Template '{template_name}' is banned. "
                f"Use 'database-{database_name}.html' instead for database-specific templates."
            )

        # Check naming conventions
        if template_name.startswith("database-") or template_name.startswith("table-"):
            if not template_name.startswith(
                f"database-{database_name}"
            ) and not template_name.startswith(f"table-{database_name}"):
                result.warnings.append(
                    f"Template '{template_name}' should include database name "
                    f"for clarity: 'database-{database_name}.html'"
                )

        # Check for safe naming patterns
        safe_patterns = [
            f"database-{database_name}",
            f"table-{database_name}-",
            "custom-",
            "_partial-",
        ]

        if not any(template_name.startswith(pattern) for pattern in safe_patterns):
            result.warnings.append(
                f"Template '{template_name}' doesn't follow recommended naming patterns. "
                f"Consider using database-specific or custom- prefixes."
            )

        return result

    def validate_metadata(self, metadata: Dict[str, Any]) -> ValidationResult:
        """Validate metadata structure and content."""
        result = ValidationResult(is_valid=True)

        # Check if it's a complete Datasette metadata structure
        for field in self.REQUIRED_METADATA_FIELDS:
            if field not in metadata:
                result.warnings.append(f"Recommended field '{field}' missing from metadata")

        # Validate JSON structure
        try:
            json.dumps(metadata)
        except (TypeError, ValueError) as e:
            result.is_valid = False
            result.errors.append(f"Invalid JSON structure: {e}")

        # Check for proper CSS/JS URL patterns
        if "extra_css_urls" in metadata:
            for url in metadata["extra_css_urls"]:
                if not url.startswith("/static/databases/"):
                    result.warnings.append(
                        f"CSS URL '{url}' should start with '/static/databases/' for proper loading"
                    )

        if "extra_js_urls" in metadata:
            for url in metadata["extra_js_urls"]:
                if not url.startswith("/static/databases/"):
                    result.warnings.append(
                        f"JS URL '{url}' should start with '/static/databases/' for proper loading"
                    )

        return result

    def validate_file_structure(
        self, customization_path: Path, database_name: str
    ) -> ValidationResult:
        """Validate the file structure of a customization."""
        result = ValidationResult(is_valid=True)

        if not customization_path.exists():
            result.is_valid = False
            result.errors.append(f"Customization path does not exist: {customization_path}")
            return result

        # Check for expected structure
        expected_dirs = ["templates", "static"]
        existing_dirs = [d.name for d in customization_path.iterdir() if d.is_dir()]

        for dir_name in existing_dirs:
            if dir_name not in expected_dirs and dir_name != "metadata.json":
                result.warnings.append(f"Unexpected directory: {dir_name}")

        # Validate templates
        templates_dir = customization_path / "templates"
        if templates_dir.exists():
            for template_file in templates_dir.glob("*.html"):
                template_result = self.validate_template_name(template_file.name, database_name)
                result.errors.extend(template_result.errors)
                result.warnings.extend(template_result.warnings)

        # Validate metadata.json if present
        metadata_file = customization_path / "metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file) as f:
                    metadata = json.load(f)
                metadata_result = self.validate_metadata(metadata)
                result.errors.extend(metadata_result.errors)
                result.warnings.extend(metadata_result.warnings)
            except (json.JSONDecodeError, IOError) as e:
                result.is_valid = False
                result.errors.append(f"Error reading metadata.json: {e}")

        return result


class ZeekerGenerator:
    """Generates Zeeker customization assets."""

    def __init__(self, database_name: str, output_path: Path):
        self.database_name = database_name
        self.sanitized_name = ZeekerValidator.sanitize_database_name(database_name)
        self.output_path = output_path
        self.customization = DatabaseCustomization(database_name, output_path)

    def create_base_structure(self) -> None:
        """Create the basic directory structure for customization."""
        dirs = [
            self.output_path,
            self.output_path / "templates",
            self.output_path / "static",
            self.output_path / "static" / "images",
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

    def generate_metadata_template(
        self,
        title: str,
        description: str,
        license_type: str = "CC-BY-4.0",
        source_url: Optional[str] = None,
        extra_css: Optional[List[str]] = None,
        extra_js: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate a complete metadata.json template."""
        metadata = {
            "title": title,
            "description": description,
            "license": license_type,
            "license_url": f"https://creativecommons.org/licenses/{license_type.lower()}/",
        }

        if source_url:
            metadata["source_url"] = source_url

        # Add CSS/JS URLs with proper paths
        if extra_css:
            metadata["extra_css_urls"] = [
                f"/static/databases/{self.sanitized_name}/{css}" for css in extra_css
            ]

        if extra_js:
            metadata["extra_js_urls"] = [
                f"/static/databases/{self.sanitized_name}/{js}" for js in extra_js
            ]

        # Add database-specific metadata
        metadata["databases"] = {self.database_name: {"description": description, "title": title}}

        return metadata

    def generate_css_template(
        self,
        primary_color: str = "#3498db",
        accent_color: str = "#e74c3c",
        include_examples: bool = True,
    ) -> str:
        """Generate a CSS template with best practices."""
        css_template = f"""/* Custom styles for {self.database_name} database */

/* CSS Custom Properties for theming */
:root {{
    --color-accent-primary: {primary_color};
    --color-accent-secondary: {accent_color};
    --font-family-custom: 'Segoe UI', system-ui, sans-serif;
}}

/* Scope styles to this database to avoid conflicts */
[data-database="{self.sanitized_name}"] {{
    /* Database-specific styles here */
}}

"""

        if include_examples:
            css_template += f"""
/* Example: Custom header styling */
.page-database[data-database="{self.sanitized_name}"] .database-title {{
    color: var(--color-accent-primary);
    font-family: var(--font-family-custom);
    text-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
}}

/* Example: Custom table styling */
.page-database[data-database="{self.sanitized_name}"] .card {{
    border-left: 4px solid var(--color-accent-primary);
    transition: transform 0.2s ease;
}}

.page-database[data-database="{self.sanitized_name}"] .card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}}

/* Example: Custom button styling */
.page-database[data-database="{self.sanitized_name}"] .btn-primary {{
    background-color: var(--color-accent-primary);
    border-color: var(--color-accent-primary);
}}

/* Responsive design considerations */
@media (max-width: 768px) {{
    .page-database[data-database="{self.sanitized_name}"] .database-title {{
        font-size: 1.5rem;
    }}
}}
"""

        return css_template

    def generate_js_template(self, include_examples: bool = True) -> str:
        """Generate a JavaScript template with best practices."""
        js_template = f"""// Custom JavaScript for {self.database_name} database

// Defensive programming - ensure we're on the right database
function isDatabasePage() {{
    return window.location.pathname.includes('/{self.database_name}') ||
           document.body.dataset.database === '{self.sanitized_name}';
}}

// Main initialization
document.addEventListener('DOMContentLoaded', function() {{
    if (!isDatabasePage()) {{
        return; // Exit if not our database
    }}

    console.log('Custom JS loaded for {self.database_name} database');

    // Initialize custom features
    initCustomFeatures();
}});

function initCustomFeatures() {{
    // Your custom functionality here
}}

"""

        if include_examples:
            js_template += f"""
// Example: Enhanced search functionality
function enhanceSearchInput() {{
    const searchInput = document.querySelector('.hero-search-input');
    if (searchInput) {{
        searchInput.placeholder = 'Search {self.database_name}...';

        // Add search suggestions or autocomplete
        searchInput.addEventListener('input', function(e) {{
            // Your search enhancement logic
            console.log('Search query:', e.target.value);
        }});
    }}
}}

// Example: Custom table enhancements
function enhanceTables() {{
    const tables = document.querySelectorAll('.table-wrapper table');
    tables.forEach(table => {{
        // Add custom sorting, filtering, or styling
        table.classList.add('enhanced-table');

        // Example: Click to highlight rows
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {{
            row.addEventListener('click', function() {{
                // Remove highlight from other rows
                rows.forEach(r => r.classList.remove('highlighted'));
                // Add highlight to clicked row
                this.classList.add('highlighted');
            }});
        }});
    }});
}}

// Example: Add custom navigation
function addCustomNavigation() {{
    const nav = document.querySelector('.nav');
    if (nav) {{
        const customLink = document.createElement('a');
        customLink.href = '/custom-dashboard';
        customLink.textContent = 'Dashboard';
        customLink.className = 'nav-link';
        nav.appendChild(customLink);
    }}
}}

// Export functions for use in other scripts if needed
window.{self.sanitized_name.replace('-', '_')}Utils = {{
    enhanceSearchInput,
    enhanceTables,
    addCustomNavigation
}};
"""

        return js_template

    def generate_database_template(self, custom_title: Optional[str] = None) -> str:
        """Generate a database-specific template."""
        title = custom_title or f"{self.database_name.title()} Database"

        return f"""{{%% extends "default:database.html" %%}}

{{%% block extra_head %%}}
{{{{ super() }}}}
<meta name="description" content="Custom database: {self.database_name}">
<meta name="keywords" content="{self.database_name}, database, search">
{{%% endblock %%}}

{{%% block content %%}}
<div class="custom-database-header">
    <h1>📊 {title}</h1>
    <p>Welcome to the {self.database_name} database</p>
</div>

{{{{ super() }}}}

<div class="custom-database-footer">
    <p>Custom content for {self.database_name}</p>
</div>
{{%% endblock %%}}

{{%% block extra_script %%}}
{{{{ super() }}}}
<script>
// Database-specific inline scripts can go here
console.log('Database template loaded for {self.database_name}');
</script>
{{%% endblock %%}}
"""

    def save_customization(
        self,
        metadata: Optional[Dict[str, Any]] = None,
        css_content: Optional[str] = None,
        js_content: Optional[str] = None,
        templates: Optional[Dict[str, str]] = None,
    ) -> None:
        """Save all customization files to disk."""
        self.create_base_structure()

        # Save metadata.json
        if metadata:
            metadata_path = self.output_path / "metadata.json"
            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Save CSS
        if css_content:
            css_path = self.output_path / "static" / "custom.css"
            with open(css_path, "w", encoding="utf-8") as f:
                f.write(css_content)

        # Save JavaScript
        if js_content:
            js_path = self.output_path / "static" / "custom.js"
            with open(js_path, "w", encoding="utf-8") as f:
                f.write(js_content)

        # Save templates
        if templates:
            for template_name, template_content in templates.items():
                template_path = self.output_path / "templates" / template_name
                with open(template_path, "w", encoding="utf-8") as f:
                    f.write(template_content)


class ZeekerDeployer:
    """Handles deployment of customizations to S3."""

    def __init__(self):
        # Get S3 configuration from environment variables
        self.bucket_name = os.getenv("S3_BUCKET")
        if not self.bucket_name:
            raise ValueError("S3_BUCKET environment variable is required")

        self.endpoint_url = os.getenv("S3_ENDPOINT_URL")
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        if not access_key or not secret_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
            )

        # Create S3 client with custom endpoint if specified
        client_kwargs = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
        }
        if self.endpoint_url:
            client_kwargs["endpoint_url"] = self.endpoint_url

        self.s3_client = boto3.client("s3", **client_kwargs)

    def upload_customization(
        self, local_path: Path, database_name: str, dry_run: bool = False
    ) -> ValidationResult:
        """Upload customization files to S3."""
        result = ValidationResult(is_valid=True)

        if not local_path.exists():
            result.is_valid = False
            result.errors.append(f"Local path does not exist: {local_path}")
            return result

        s3_prefix = f"assets/databases/{database_name}/"

        for file_path in local_path.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(local_path)
                s3_key = s3_prefix + str(relative_path).replace("\\", "/")

                if dry_run:
                    result.info.append(
                        f"Would upload: {file_path} -> s3://{self.bucket_name}/{s3_key}"
                    )
                else:
                    try:
                        self.s3_client.upload_file(str(file_path), self.bucket_name, s3_key)
                        result.info.append(
                            f"Uploaded: {file_path} -> s3://{self.bucket_name}/{s3_key}"
                        )
                    except Exception as e:
                        result.errors.append(f"Failed to upload {file_path}: {e}")
                        result.is_valid = False

        return result

    def list_customizations(self) -> List[str]:
        """List all database customizations in S3."""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix="assets/databases/", Delimiter="/"
            )

            databases = []
            for prefix in response.get("CommonPrefixes", []):
                db_name = prefix["Prefix"].split("/")[-2]
                databases.append(db_name)

            return sorted(databases)
        except Exception as e:
            print(f"Error listing customizations: {e}")
            return []


# CLI Interface
@click.group()
def cli():
    """Zeeker Database Customization Tool."""
    pass


@cli.command()
@click.argument("database_name")
@click.argument("output_path", type=click.Path())
@click.option("--title", help="Database title")
@click.option("--description", help="Database description")
@click.option("--primary-color", default="#3498db", help="Primary color")
@click.option("--accent-color", default="#e74c3c", help="Accent color")
def generate(database_name, output_path, title, description, primary_color, accent_color):
    """Generate a new database customization."""
    output_dir = Path(output_path)
    generator = ZeekerGenerator(database_name, output_dir)

    # Generate metadata
    metadata = generator.generate_metadata_template(
        title=title or f"{database_name.title()} Database",
        description=description or f"Custom database for {database_name}",
        extra_css=["custom.css"],
        extra_js=["custom.js"],
    )

    # Generate CSS and JS
    css_content = generator.generate_css_template(primary_color, accent_color)
    js_content = generator.generate_js_template()

    # Generate database template
    db_template = generator.generate_database_template()
    templates = {f"database-{generator.sanitized_name}.html": db_template}

    # Save everything
    generator.save_customization(metadata, css_content, js_content, templates)

    click.echo(f"Generated customization for '{database_name}' in {output_dir}")


@cli.command()
@click.argument("customization_path", type=click.Path(exists=True))
@click.argument("database_name")
def validate(customization_path, database_name):
    """Validate a database customization."""
    validator = ZeekerValidator()
    result = validator.validate_file_structure(Path(customization_path), database_name)

    if result.errors:
        click.echo("❌ Validation failed:")
        for error in result.errors:
            click.echo(f"  ERROR: {error}")

    if result.warnings:
        click.echo("⚠️ Warnings:")
        for warning in result.warnings:
            click.echo(f"  WARNING: {warning}")

    if result.info:
        for info in result.info:
            click.echo(f"  INFO: {info}")

    if result.is_valid and not result.warnings:
        click.echo("✅ Validation passed!")

    return result.is_valid


@cli.command()
@click.argument("local_path", type=click.Path(exists=True))
@click.argument("database_name")
@click.option("--dry-run", is_flag=True, help="Show what would be uploaded without uploading")
def deploy(local_path, database_name, dry_run):
    """Deploy customization to S3.

    Requires environment variables:
    - S3_BUCKET: S3 bucket name
    - S3_ENDPOINT_URL: S3 endpoint URL (optional, defaults to AWS)
    - AWS_ACCESS_KEY_ID: AWS access key
    - AWS_SECRET_ACCESS_KEY: AWS secret key
    """
    try:
        deployer = ZeekerDeployer()
    except ValueError as e:
        click.echo(f"❌ Configuration error: {e}")
        click.echo("Please set the required environment variables:")
        click.echo("  - S3_BUCKET")
        click.echo("  - AWS_ACCESS_KEY_ID")
        click.echo("  - AWS_SECRET_ACCESS_KEY")
        click.echo("  - S3_ENDPOINT_URL (optional)")
        return

    result = deployer.upload_customization(Path(local_path), database_name, dry_run)

    if result.errors:
        click.echo("❌ Deployment failed:")
        for error in result.errors:
            click.echo(f"  ERROR: {error}")

    for info in result.info:
        click.echo(f"  {info}")

    if result.is_valid:
        if dry_run:
            click.echo("✅ Dry run completed successfully!")
        else:
            click.echo(f"✅ Deployment completed successfully to {deployer.bucket_name}!")


@cli.command()
def list_databases():
    """List all database customizations in S3.

    Requires environment variables:
    - S3_BUCKET: S3 bucket name
    - S3_ENDPOINT_URL: S3 endpoint URL (optional, defaults to AWS)
    - AWS_ACCESS_KEY_ID: AWS access key
    - AWS_SECRET_ACCESS_KEY: AWS secret key
    """
    try:
        deployer = ZeekerDeployer()
    except ValueError as e:
        click.echo(f"❌ Configuration error: {e}")
        click.echo("Please set the required environment variables:")
        click.echo("  - S3_BUCKET")
        click.echo("  - AWS_ACCESS_KEY_ID")
        click.echo("  - AWS_SECRET_ACCESS_KEY")
        click.echo("  - S3_ENDPOINT_URL (optional)")
        return

    databases = deployer.list_customizations()

    if databases:
        click.echo(f"Database customizations found in {deployer.bucket_name}:")
        for db in databases:
            click.echo(f"  - {db}")
    else:
        click.echo(f"No database customizations found in {deployer.bucket_name}.")


if __name__ == "__main__":
    cli()
