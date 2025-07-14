from urllib.parse import urlencode

import requests
from lib.sign import Sign
from lib.utils import getUNIX, md5stub



ts=getUNIX(False)
rticket=getUNIX(True)

params = f"os_api=25&device_type=SM-G930F&ssmix=a&manifest_version_code=2019091803&dpi=560&carrier_region=FR&uoo=0&region=US&carrier_region_v2=208&app_name=musical_ly&version_name=13.1.3&timezone_offset=3600&ts={ts}&ab_version=13.1.3&pass-route=1&pass-region=1&is_my_cn=0&ac2=wifi5g&ac=wifi&app_type=normal&channel=googleplay&update_version_code=2019091803&_rticket={rticket}&device_platform=android&iid=7510095057765779205&build_number=13.1.3&locale=en&version_code=130103&timezone_name=Europe%2FParis&openudid=4574be359e497627&device_id=7510093320766195206&sys_region=US&app_language=en&resolution=1440*2560&device_brand=samsung&language=en&os_version=7.1.2&aid=1233&mcc_mnc=20801"

body = urlencode({"aweme_id":"7526560697086446903","text":"Good sloth"})

headers = Sign(params,headers={
            'x-ss-req-ticket': str(getUNIX(True)),
            'x-ss-stub': md5stub(body),
            'Passport-Sdk-Version': '19',
            'Sdk-Version': '2',
            'Multi_login': '1',
            'X-Tt-Dm-Status': 'login=1;ct=1;rt=1',
            'X-Vc-Bdturing-Sdk-Version': '2.3.4.i18n',
            'X-Tt-Store-Region': 'au',
            'X-Tt-Store-Region-Src': 'uid',
            'User-Agent': f'com.zhiliaoapp.musically/320905 (Linux; U; Android 7.1.2; en_US; SM-G930F; Build/RP1A.200720.012;tt-ok/3.12.13.4-tiktok)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            "X-Tt-Token":"03b418a67a6f330e3c87c997d3a38af867023f0760b696f42bba7d96dacae6b19662092940559e7afad8ffd53f037622d37abbebc81abcec97e25240925d43c47ad885f4cb0dd55269a329efa3c2526a9aff1126210ccf8da8a1f987df9a6139219b7--0a4e0a20663952d025253e148fea701c7f766f0a8477d42d86be6c83a33ad64fd12acd021220ee34645304f22a3dd8ca168149a70260df7076122e6bf54b05959254ee5245311801220674696b746f6b-3.0.0", # Replace with your TT Token
            "Cookie":"sessionid="
        })
response = requests.post(
            f'https://api16-normal-c-alisg.tiktokv.com/aweme/v1/comment/publish/?{params}',
            headers=headers,
            data=body,
            #proxies={'http': 'http://' + select_proxy, 'https': 'http://' + select_proxy}
        )
print(response.text)