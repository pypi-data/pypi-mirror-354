# eops/cli.py
import typer

main_app = typer.Typer(help="Eops - A quantitative trading framework.")

@main_app.command()
def run(
    config_file: str = typer.Argument(..., help="Path to the configuration file."),
    backtest: bool = typer.Option(False, "--backtest", help="Run in backtesting mode."),
):
    """
    Run a trading strategy from a configuration file.
    """
    typer.echo(f"🚀 Starting Eops runner...")
    typer.echo(f"⚙️ Config file: {config_file}")
    
    if backtest:
        typer.secho("MODE: Backtesting", fg=typer.colors.YELLOW)
        # 在这里调用回测引擎的逻辑 (后续实现)
        typer.echo("Backtesting engine is not implemented yet.")
    else:
        typer.secho("MODE: Live Trading", fg=typer.colors.GREEN)
        # 在这里调用实盘引擎的逻辑 (后续实现)
        typer.echo("Live trading engine is not implemented yet.")
        
    typer.echo("✅ Eops run finished.")

@main_app.command()
def info():
    """Displays information about eops."""
    # 我们可以在 __init__.py 中定义版本号
    from . import __version__
    typer.echo(f"Eops Quant Trading Library v{__version__}")

# (可选) 你可以现在就加上这个，以后会用到
if __name__ == "__main__":
    main_app()