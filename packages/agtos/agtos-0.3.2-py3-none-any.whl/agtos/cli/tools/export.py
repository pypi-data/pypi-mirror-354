"""Tool catalog export functionality.

AI_CONTEXT:
    This module handles exporting the complete tool catalog to various
    formats for documentation or external use. Supports JSON, YAML,
    and Markdown formats with full metadata preservation.
    
    Export includes:
    - All tools with descriptions and schemas
    - Service grouping
    - Category statistics
    - Aliases and display names
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

import typer
from rich.console import Console

from ...metamcp.server import MetaMCPServer
from ...metamcp.categories import CategoryManager
from ...errors import handle_error

console = Console()


def export_tools(
    output: Path = typer.Option(
        Path("tools.json"), "--output", "-o",
        help="Output file path"
    ),
    output_format: str = typer.Option(
        "json", "--format", "-f",
        help="Export format: json, yaml, markdown"
    )
):
    """Export tool catalog to a file.
    
    AI_CONTEXT:
        Exports all discovered tools with their metadata, categories,
        and documentation to various formats for external use.
    """
    try:
        asyncio.run(_export_tools_async(
            output=output,
            format=output_format
        ))
    except Exception as e:
        handle_error(e)


async def _export_tools_async(output: Path, format: str):
    """Export tools to file.
    
    AI_CONTEXT:
        Collects all tool information including metadata, categories,
        and schemas, then exports to the requested format. Supports
        JSON for programmatic use, YAML for configuration, and
        Markdown for documentation.
    """
    # Create server and discover tools
    server = MetaMCPServer(port=0)
    await server.initialize()
    category_manager = CategoryManager()
    
    # Collect all tools with metadata
    export_data = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "services": {},
        "categories": {},
        "total_tools": 0
    }
    
    # Collect tools by service
    for service_name, service_info in server.registry.services.items():
        service_tools = []
        
        for tool in service_info.tools:
            # Categorize
            categories = category_manager.categorize_tool(tool)
            
            tool_data = {
                "name": tool.name,
                "description": tool.description,
                "categories": [cat.value for cat in categories]
            }
            
            if hasattr(tool, "displayName"):
                tool_data["displayName"] = tool.displayName
            
            if hasattr(tool, "aliases"):
                tool_data["aliases"] = tool.aliases
            
            if hasattr(tool, "inputSchema"):
                tool_data["inputSchema"] = tool.inputSchema
            
            service_tools.append(tool_data)
        
        export_data["services"][service_name] = {
            "tools": service_tools,
            "tool_count": len(service_tools)
        }
        
        export_data["total_tools"] += len(service_tools)
    
    # Add category stats
    export_data["categories"] = category_manager.get_category_stats()
    
    # Export based on format
    if format == "json":
        _export_json(export_data, output)
    elif format == "yaml":
        _export_yaml(export_data, output)
    elif format == "markdown":
        _export_markdown(export_data, output)
    else:
        console.print(f"[red]Unsupported format: {format}[/red]")


def _export_json(data: dict, output: Path):
    """Export data as JSON.
    
    AI_CONTEXT:
        Writes formatted JSON with proper indentation for readability.
    """
    output.write_text(json.dumps(data, indent=2))
    console.print(f"[green]✓[/green] Exported {data['total_tools']} tools to {output}")


def _export_yaml(data: dict, output: Path):
    """Export data as YAML.
    
    AI_CONTEXT:
        Exports to YAML format if the yaml package is available.
        YAML is useful for configuration files and is more human-readable
        than JSON.
    """
    try:
        import yaml
        output.write_text(yaml.dump(data, default_flow_style=False))
        console.print(f"[green]✓[/green] Exported {data['total_tools']} tools to {output}")
    except ImportError:
        console.print("[red]YAML export requires PyYAML: pip install pyyaml[/red]")


def _export_markdown(data: dict, output: Path):
    """Export data as Markdown documentation.
    
    AI_CONTEXT:
        Creates comprehensive Markdown documentation with table of contents,
        service sections, and tool details including parameters.
    """
    md_content = _generate_markdown_catalog(data)
    output.write_text(md_content)
    console.print(f"[green]✓[/green] Exported {data['total_tools']} tools to {output}")


def _generate_markdown_catalog(data: dict) -> str:
    """Generate markdown documentation for tools.
    
    AI_CONTEXT:
        Creates a structured Markdown document with:
        - Header and metadata
        - Table of contents
        - Service sections with tool details
        - Parameter documentation for each tool
    """
    lines = []
    
    lines.append("# agtos Tool Catalog")
    lines.append(f"\nGenerated at: {data['generated_at']}")
    lines.append(f"\nTotal tools: {data['total_tools']}")
    
    # Table of contents
    lines.append("\n## Table of Contents\n")
    for service_name in sorted(data["services"].keys()):
        anchor = service_name.lower().replace(" ", "-").replace("_", "-")
        lines.append(f"- [{service_name}](#{anchor})")
    
    # Service sections
    for service_name, service_data in sorted(data["services"].items()):
        lines.append(f"\n## {service_name}")
        lines.append(f"\nTools: {service_data['tool_count']}")
        
        for tool in service_data["tools"]:
            lines.append(f"\n### {tool['name']}")
            
            if "displayName" in tool:
                lines.append(f"\n**Display Name:** {tool['displayName']}")
            
            if "aliases" in tool:
                lines.append(f"\n**Aliases:** {', '.join(tool['aliases'])}")
            
            lines.append(f"\n**Categories:** {', '.join(tool['categories'])}")
            
            lines.append(f"\n**Description:** {tool['description']}")
            
            if "inputSchema" in tool:
                lines.append("\n**Parameters:**")
                lines.append("```json")
                lines.append(json.dumps(tool["inputSchema"], indent=2))
                lines.append("```")
    
    return "\n".join(lines)