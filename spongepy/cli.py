import click
import pandas as pd
from . import cleaner as cl
from .utils import read_into_df

@click.command()
@click.option('--file', '-f', required=True, help='Input data file ')
@click.option('--clean', is_flag=True, help='Clean the data based on a configuration file or predefined rules')
@click.option('--config', '-c', default=None, help='Input configuration file (JSON format)')
@click.option('--stats', '-s', is_flag=True, help='Show general statistics')
@click.option('--details', '-d', is_flag=True, help='Show detailed statistics')
@click.option('--export', '-e', default=None, metavar='FILE', help='chose export name')


def cli(file, clean, details, config, stats, export):
    """SpongePy - data processing tool"""
    print("\033[1;35m")
    print(r"""    
       _____                              _____        
      / ____|                            |  __ \       
     | (___  _ __   ___  _ __   __ _  ___| |__) |   _  
      \___ \| '_ \ / _ \| '_ \ / _` |/ _ \  ___/ | | | 
      ____) | |_) | (_) | | | | (_| |  __/ |   | |_| | 
     |_____/| .__/ \___/|_| |_|\__, |\___|_|    \__, | 
            | |                 __/ |            __/ | 
            |_|                |___/            |___/   
    """)
    print("\033[0m")

    df = read_into_df(file)

    if clean:
        if config:
            click.echo(f"Cleaning data with config: {config}")
            cl.configured_cleaning(df, config, file, export)
        else:
            click.echo("Cleaning data with default parameters")
            cl.default_cleaning(df, file, export)

    if details:
        click.echo("Showing detailed statistics:")
        cl.show_general_stats(df, True)
    elif stats:
        click.echo("Showing general statistics:")
        cl.show_general_stats(df, False)

    return df

if __name__ == '__main__':
    cli()