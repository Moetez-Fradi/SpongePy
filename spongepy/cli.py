import click
import pandas as pd
from . import cleaner as cl

@click.command()
@click.option('--file', '-f', required=True, help='Input data file ')
@click.option('--clean', is_flag=True, help='Clean the data')
@click.option('--config', '-c', default=None, help='Configuration file (YAML format)')
@click.option('--stats', '-s', is_flag=True, help='Show general statistics')
def cli(file, clean, config, stats):
    """SpongePy - Your data processing tool"""
    print("\033[1;35m")
    print(r"""    
        _____                             _____        
      / ____|                            |  __ \       
     | (___  _ __   ___  _ __   __ _  ___| |__) |   _  
      \___ \| '_ \ / _ \| '_ \ / _` |/ _ \  ___/ | | | 
      ____) | |_) | (_) | | | | (_| |  __/ |   | |_| | 
     |_____/| .__/ \___/|_| |_|\__, |\___|_|    \__, | 
            | |                 __/ |            __/ | 
            |_|                |___/            |___/   
    """)
    print("\033[0m")

    df = cl.read_into_df(file)

    if clean:
        if config:
            click.echo(f"Cleaning data with config: {config}")
        else:
            click.echo("Cleaning data with default parameters")

    if stats:
        click.echo("Showing general statistics:")
        cl.show_general_stats(df)
    return df

if __name__ == '__main__':
    cli()