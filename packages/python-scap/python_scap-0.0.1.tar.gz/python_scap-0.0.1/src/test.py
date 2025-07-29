from python_scap._core.http import BaseClient
from python_scap.clients.cpe import NvdCpeClient

from pathlib import Path
import json


async def test():
    URL = 'https://nvd.nist.gov/feeds/json/cpe/2.0/nvdcpe-2.0.zip'
    client = BaseClient()
    for item in await client.get(URL):
        *folders, filename = item['filename'].split('/')
        if folders:
            Path.mkdir(Path('.').joinpath(*folders), exist_ok=True)

        with open(item['filename'], 'wb') as f:
            f.write(item['content'])
            # f.write(json.dumps(xmltodict.parse(item['content']), indent=2).encode('utf-8'))


def test_json():
    from python_scap.schemas.cpe import CpeItem

    count = set()
    output = list()

    for file in sorted(Path('.').glob('**/*.json')):
        print(file)

        with open(file, 'r') as f:
            data = json.load(f)
            for product in data['products']:
                try:
                    item = CpeItem(**product['cpe'])
                except ValueError as e:
                    print(file)
                    print(e)
                    print(product['cpe'])
                    return
                if item.name.startswith('cpe:2.3:o:microsoft:windows_nt:4.0'):
                    output.append(product['cpe'])

                # if item.deprecated_by:
                #     if len(item.deprecated_by) > 1:
                #         print(item.deprecated_by)
                #         print(item.deprecates)
                #         return
                #     # print(item)
                #     # return

    with open('cpe-test.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(count)



def test_client():
    client = NvdCpeClient()
    for item in client.get_cpe_items():
        print(item.cpe23Uri, item.title)

if __name__ == '__main__':
    import asyncio
    # asyncio.run(test())
    test_json()
