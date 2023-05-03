# nspyre Template
An [nspyre](https://nspyre.readthedocs.io/en/latest/) experiment template.

To install, simply:
`pip install -e .`

To run the experiment, first start the instrument servers:
`python src/template/drivers/inserv1.py`
`python src/template/drivers/inserv2.py`

Run the nspyre data server:
`nspyre-dataserv`

Start the experiment GUI:
`python src/template/app.py`

