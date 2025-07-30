#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI module for Dataheroes commands.
"""

import click
from typing import Optional, Dict
from getpass import getpass
import os

from dataheroes.configuration import DataHeroesConfiguration
from dataheroes.utils import activate_account
from dataheroes.version_type import offline_version

def mask_sensitive_value(value: str) -> str:
    """Mask sensitive information by showing only the last 4 characters."""
    if not value or len(value) <= 4:
        return value
    return "*" * (len(value) - 4) + value[-4:]


class DataheroesInitCLI:
    """Interactive CLI for initializing Dataheroes configuration."""

    def __init__(self):
        self.config = DataHeroesConfiguration()
        self.sections = {
            "licensing": ["license_key"],
            "databricks": [
                "api_key",
                "workspace_url",
                "http_path",
                "catalog",
                "schema",
            ],
            "aws": ["access_key_id", "secret_access_key", "region"],
            "gcp": ["project_id", "credentials_path"],
            "azure": ["storage_connection_string"],
        }
        self.sensitive_fields = [
            "license_key",
            "api_key",
            "access_key_id",
            "secret_access_key",
            "credentials_path",
            "storage_connection_string",
        ]

    def get_current_config(self, section: str) -> Dict[str, str]:
        """Get current configuration for a section."""
        result = {}
        for param in self.sections.get(section, []):
            value = self.config.get_param_str(param, section=section)
            if value is not None:
                result[param] = value
        return result

    def display_session_config(self, section: str) -> None:
        """Display current configuration for a section."""
        config = self.get_current_config(section)
        if not config:
            click.echo(f"No existing {section} configuration found.")
            return

        click.echo(f"\nCurrent {section} configuration:")
        for param, value in config.items():
            displayed_value = (
                mask_sensitive_value(value) if param in self.sensitive_fields else value
            )
            click.echo(f"  {param}: {displayed_value}")
        click.echo("")

    def prompt_for_value(self, param: str, current_value: Optional[str] = None) -> str:
        """Prompt user for a configuration value."""
        prompt_text = f"Enter {param}"
        if current_value:
            masked_value = (
                mask_sensitive_value(current_value)
                if param in self.sensitive_fields
                else current_value
            )
            prompt_text += f" (current: {masked_value})"
        prompt_text += ": "

        if param in self.sensitive_fields:
            value = getpass(prompt_text)
        else:
            value = click.prompt(prompt_text, default="", show_default=False)

        # If user didn't enter anything and there's a current value, keep the current value
        if not value and current_value:
            return current_value
        return value

    def update_config(self, section: str, param: str, value: str) -> None:
        """Update configuration with confirmation for sensitive values."""
        if param in self.sensitive_fields:
            if click.confirm(f"Are you sure you want to update {param}?", default=True):
                self.config.update_create_config_file(section, param, value)
                click.echo(f"{param} updated successfully.")
            else:
                click.echo(f"{param} update cancelled.")
        else:
            self.config.update_create_config_file(section, param, value)
            click.echo(f"{param} updated successfully.")

    def setup_license(self) -> None:
        """
        Activate Dataheroes account using email.

        Uses the activate_account function from utils.py to validate and activate
        the license with the Dataheroes licensing server.
        """
        if offline_version():
            click.echo("Dataheroes is running in offline mode. License activation is not required.")
            return

        click.echo("\n=== Dataheroes License Activation ===")

        # Display current license if available
        current_license = self.config.get_param_str("license_key", section="licensing")
        if current_license:
            click.echo(
                f"\nCurrent license key: {mask_sensitive_value(current_license)}"
            )

        # Prompt for email
        email = click.prompt("Enter your email address", default="", show_default=False)

        if not email:
            click.echo("Email is required for license activation. Operation cancelled.")
            return

        # Attempt to activate the account with the provided email
        try:
            click.echo("Activating license with Dataheroes server...")
            activate_account(email=email)
            click.echo("License activated successfully!")

            # Display the new license key
            new_license = self.config.get_param_str("license_key", section="licensing")
            if new_license and new_license != current_license:
                click.echo(f"New license key: {mask_sensitive_value(new_license)}")
        except RuntimeError as e:
            click.echo(f"Error activating license: {str(e)}", err=True)

    def setup_service_provider(self, provider: str) -> None:
        """Setup cloud provider credentials."""
        click.echo(f"\n=== {provider.upper()} Configuration ===")
        self.display_session_config(provider)

        current_config = self.get_current_config(provider)
        updated = False

        for param in self.sections[provider]:
            value = self.prompt_for_value(param, current_config.get(param))
            if value:
                self.update_config(provider, param, value)
                updated = True

        if not updated:
            click.echo(f"No changes made to {provider.upper()} configuration.")

    def display_config(self) -> None:
        """View all current configuration."""
        click.echo("\n=== Current Configuration ===")

        for section in self.sections:
            config = self.get_current_config(section)
            if config:
                click.echo(f"\n{section.upper()} Configuration:")
                for param, value in config.items():
                    displayed_value = (
                        mask_sensitive_value(value)
                        if param in self.sensitive_fields
                        else value
                    )
                    click.echo(f"  {param}: {displayed_value}")

    def run_interactive(self) -> None:
        """Run the interactive CLI menu."""
        click.echo("Welcome to Dataheroes Configuration Setup")
        menu = []
        if not offline_version():
            menu.append("Activate Dataheroes account (using email)")

        menu += [
            "Setup Databricks credentials",
            "Setup AWS credentials",
            "Setup GCP credentials",
            "Setup Azure credentials",
            "View current configuration",
            "Exit",
        ]
        # Create a mapping of menu options to their corresponding functions
        menu_actions = {}
        for i, option in enumerate(menu, start=1):
            menu_actions[i] = option

        while True:
            click.echo("\nPlease select an option:")
            for i, option in enumerate(menu, start=1):
                click.echo(f"{i}. {option}")

            # Default choice is the last option (Exit)
            default_choice = len(menu)
            choice = click.prompt("Enter your choice", type=int, default=default_choice)

            if choice not in menu_actions:
                click.echo("Invalid choice. Please try again.")
                continue

            selected_option = menu_actions[choice]

            if selected_option == "Exit":
                click.echo("Exiting Dataheroes configuration setup.")
                break
            elif selected_option == "Activate Dataheroes account (using email)":
                self.setup_license()
            elif selected_option == "Setup Databricks credentials":
                self.setup_service_provider("databricks")
            elif selected_option == "Setup AWS credentials":
                self.setup_service_provider("aws")
            elif selected_option == "Setup GCP credentials":
                self.setup_service_provider("gcp")
            elif selected_option == "Setup Azure credentials":
                self.setup_service_provider("azure")
            elif selected_option == "View current configuration":
                self.display_config()
            else:
                click.echo("Invalid choice. Please try again.")


@click.command()
@click.option("--email", help="Email for license activation")
@click.option("--databricks_api_key", help="Set Databricks API key")
@click.option("--databricks_workspace_url", help="Set Databricks workspace URL")
@click.option("--databricks_http_path", help="Set Databricks HTTP path")
@click.option("--databricks_catalog", help="Set Databricks catalog")
@click.option("--databricks_schema", help="Set Databricks schema")
@click.option("--aws_access_key_id", help="Set AWS access key ID")
@click.option("--aws_secret_access_key", help="Set AWS secret access key")
@click.option("--aws_region", help="Set AWS region")
@click.option("--gcp_project_id", help="Set GCP project ID")
@click.option("--gcp_credentials_path", help="Set GCP credentials path")
@click.option("--azure_storage_connection_string", help="Set Azure storage connection string")
# @click.option("--azure_subscription_id", help="Set Azure subscription ID")
# @click.option("--azure_tenant_id", help="Set Azure tenant ID")
# @click.option("--azure_client_id", help="Set Azure client ID")
# @click.option("--azure_client_secret", help="Set Azure client secret")
def main(**kwargs):
    """
    Initialize Dataheroes configuration.

    This command provides a menu-driven interface for configuring your Dataheroes account
    and connection credentials. You can also use command-line options to set specific
    configuration values directly. If any command-line options are provided, the configuration
    file will be updated with the new values and the interactive menu will not be shown.

    If no command-line options are provided and no configuration file is found,
    it will prompt only for email activation.
    """
    cli = DataheroesInitCLI()

    # Check if any command-line options were provided
    options_provided = any(kwargs.values())

    if options_provided:
        # Process command-line options
        config = DataHeroesConfiguration()
        email = kwargs.pop("email", None)

        # If email is provided, activate the account
        if email:
            try:
                click.echo(f"Activating license with email: {email}")
                if offline_version():
                    click.echo("Dataheroes is running in offline mode. License activation is not required.")
                else:
                    activate_account(email=email)
                    click.echo("License activated successfully!")
            except RuntimeError as e:
                click.echo(f"Error activating license: {str(e)}", err=True)
        # TODO: Update the config file only after I have the confirmation from the user with a single file opening.
        # Process other configuration options
        for key, value in kwargs.items():
            if value is not None:
                if key.startswith("databricks_"):
                    param = key.replace("databricks_", "")
                    config.update_create_config_file("databricks", param, value)
                    click.echo(f"Updated databricks.{param}")
                elif key.startswith("aws_"):
                    param = key.replace("aws_", "")
                    config.update_create_config_file("aws", param, value)
                    click.echo(f"Updated aws.{param}")
                elif key.startswith("gcp_"):
                    param = key.replace("gcp_", "")
                    config.update_create_config_file("gcp", param, value)
                    click.echo(f"Updated gcp.{param}")
                elif key.startswith("azure_"):
                    param = key.replace("azure_", "")
                    config.update_create_config_file("azure", param, value)
                    click.echo(f"Updated azure.{param}")
    else:
        # No command-line options provided, check for existing config file
        config_file_path = DataHeroesConfiguration.top_priority_file_path()
        if os.path.exists(config_file_path):
            # Config file exists, run the full interactive menu
            click.echo(f"Using configuration file: {config_file_path}")
            cli.run_interactive()
        else:
            # No config file found, prompt only for email activation
            cli.setup_license()


if __name__ == "__main__":
    main()
