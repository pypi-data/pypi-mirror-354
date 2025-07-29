import click
from .converter import CSV2SQL
import glob

@click.command()
@click.argument('input_files', nargs=-1, required=True)
@click.argument('output_file', type=click.Path())
@click.option('--db-type', '-d', default='mysql',
              type=click.Choice(['mysql', 'postgresql', 'sqlite', 'oracle', 'mssql']),
              help='目标数据库类型')
@click.option('--table-name', '-t', help='表名模式（使用 {filename} 作为文件名占位符）')
@click.option('--charset', '-c', help='字符集（仅 MySQL 和 PostgreSQL 支持）')
def main(input_files: tuple, output_file: str, db_type: str, 
         table_name: str = None, charset: str = None):
    """将 CSV 文件转换为 SQL 建表语句和插入语句，支持多个输入文件，可以使用通配符（如 *.csv）"""
    try:
        expanded_files = []
        for pattern in input_files:
            if '*' in pattern or '?' in pattern:
                expanded_files.extend(glob.glob(pattern))
            else:
                expanded_files.append(pattern)
        if not expanded_files:
            click.echo("错误: 没有找到匹配的 CSV 文件", err=True)
            raise click.Abort()
        converter = CSV2SQL()
        converter.convert_multiple_files(
            input_files=expanded_files,
            output_file=output_file,
            db_type=db_type,
            table_name_pattern=table_name,
            charset=charset
        )
        click.echo(f"转换完成！输出文件: {output_file}")
    except Exception as e:
        click.echo(f"错误: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    main()