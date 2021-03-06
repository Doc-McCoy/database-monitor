# database-monitor

Script simples que exibe em tempo real o conteúdo de uma tabela. Feito para agilizar a conferência em testes de insert / update / delete.

Funciona somente com o **PostgreSQL**

## Instalação:
### Criar o ambiente virtual
```shell
$python -m venv venv
$source venv/bin/activate
```

### Instalar as dependências
```shell
(venv)$pip install -r requirements.txt
```

### Criar um arquivo `config.ini` com as informações do postgres, seguindo o modelo:
```ini
[DATABASE]
host = host
user = user
password = pass
database = db
port = port
```

## Modo de usar:
```shell
(venv)$python monitor.py <nome_da_tabela_a_ser_monitorada>
```

Após isso, as atualizações em tempo real nessa tabela serão exibidas no terminal.

## Screenshot

![screenshot](https://github.com/Doc-McCoy/database-monitor/blob/master/screenshot.png)

## TODO

- [ ] Adaptar o app para se conectar com o MySQL e SQLite também.
