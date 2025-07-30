"""Console script for p1zyq."""

import sys
from pathlib import Path
import p1zyq

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import Optional, List

app = typer.Typer(
    help="Python项目模板，包含创建Python包所需的所有基础结构。",
    add_completion=True,
)
console = Console()


# CLI工具特定命令
@app.command()
def process(
    input_file: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="输入文件路径"
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="输出文件路径"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="显示详细输出"),
):
    """处理输入文件并生成输出。"""
    if verbose:
        console.print(f"处理文件: [bold]{input_file}[/bold]")

    # 这里添加文件处理逻辑

    if output_file:
        if verbose:
            console.print(f"输出保存到: [bold]{output_file}[/bold]")
    else:
        console.print("处理完成，没有指定输出文件")


@app.command()
def list_examples():
    """列出可用的示例。"""
    table = Table(title="可用示例")
    table.add_column("名称", style="cyan")
    table.add_column("描述", style="green")

    table.add_row("示例1", "示例1的描述")
    table.add_row("示例2", "示例2的描述")
    table.add_row("示例3", "示例3的描述")

    console.print(table)


# Web服务特定命令
@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="服务器主机地址"),
    port: int = typer.Option(8000, "--port", "-p", help="服务器端口"),
    reload: bool = typer.Option(True, "--reload/--no-reload", help="启用/禁用自动重载"),
):
    """启动Web服务。"""
    try:
        import uvicorn
    except ImportError:
        console.print(
            "[bold red]错误[/bold red]: uvicorn未安装，请先安装: pip install uvicorn"
        )
        return

    console.print(
        Panel(
            f"启动服务器在 [bold]http://{host}:{port}[/bold]",
            title="p1zyq Web服务",
            border_style="green",
        )
    )

    uvicorn.run("p1zyq.app:app", host=host, port=port, reload=reload)


@app.command()
def routes():
    """显示所有API路由。"""
    try:
        from p1zyq.app import app as fastapi_app
    except ImportError:
        console.print(
            "[bold red]错误[/bold red]: 未找到FastAPI应用，请确保app.py已正确配置"
        )
        return

    table = Table(title="API路由")
    table.add_column("方法", style="cyan")
    table.add_column("路径", style="green")
    table.add_column("名称", style="blue")

    for route in fastapi_app.routes:
        methods = getattr(route, "methods", ["GET"])
        path = getattr(route, "path", "/")
        name = getattr(route, "name", "")

        for method in methods:
            table.add_row(method, path, name or "-")

    console.print(table)


# 数据科学项目特定命令
@app.command()
def analyze(
    dataset: Path = typer.Argument(..., exists=True, help="数据集文件路径"),
    output_dir: Path = typer.Option(
        Path("./output"), "--output-dir", "-o", help="输出目录"
    ),
    visualize: bool = typer.Option(
        True, "--visualize/--no-visualize", help="是否生成可视化"
    ),
):
    """分析数据集并生成报告。"""
    console.print(f"分析数据集: [bold]{dataset}[/bold]")

    # 确保输出目录存在
    output_dir.mkdir(exist_ok=True, parents=True)

    # 这里添加数据分析逻辑

    console.print(f"分析结果将保存到: [bold]{output_dir}[/bold]")

    if visualize:
        console.print("正在生成数据可视化...")
        # 这里添加可视化生成逻辑


@app.command()
def train(
    dataset: Path = typer.Argument(..., exists=True, help="训练数据集路径"),
    model_output: Path = typer.Option(
        Path("./models/model.pkl"), "--model-output", "-m", help="模型输出路径"
    ),
    epochs: int = typer.Option(10, "--epochs", "-e", help="训练轮数"),
):
    """训练机器学习模型。"""
    console.print(f"使用数据集 [bold]{dataset}[/bold] 训练模型")
    console.print(f"训练轮数: [bold]{epochs}[/bold]")

    # 确保输出目录存在
    model_output.parent.mkdir(exist_ok=True, parents=True)

    # 这里添加模型训练逻辑

    console.print(f"模型将保存到: [bold]{model_output}[/bold]")


# 标准命令
@app.command()
def info():
    """显示项目信息。"""
    version = getattr(p1zyq, "__version__", "未知")

    console.print(
        Panel(
            f"""
项目名称: [bold]p1zyq[/bold]
版本: [bold]{version}[/bold]
描述: Python项目模板，包含创建Python包所需的所有基础结构。
作者: Zhou Yuanqi
        """,
            title="项目信息",
            border_style="blue",
        )
    )


# 通用命令
@app.command()
def version():
    """显示版本信息。"""
    version = getattr(p1zyq, "__version__", "未知")
    console.print(f"p1zyq v{version}")


@app.command()
def main():
    """p1zyq 的主命令。"""
    console.print(
        Panel(
            "使用 --help 查看可用命令",
            title="p1zyq",
            border_style="green",
        )
    )


def cli():
    """Entry point for console script."""
    app()


if __name__ == "__main__":
    sys.exit(cli())
