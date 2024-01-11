# SonicBooks | 声阅
<p align="center" dir="auto">
<a>
<img alt="macOS" src="https://camo.githubusercontent.com/8f36a22bb36a09701c14d3bdadf1369dc04e37f234709e5f472468c978c7ea6b/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d6d61634f532d626c61636b3f7374796c653d666c61742d737175617265266c6f676f3d6170706c65266c6f676f436f6c6f723d7768697465" data-canonical-src="https://img.shields.io/badge/-macOS-black?style=flat-square&amp;logo=apple&amp;logoColor=white" style="max-width: 100%;">
</a>
<a>
<img alt="Windows" src="https://camo.githubusercontent.com/d560472c2942f7836639fae485ae2884eaaed707f15976d8129abf2b4fb7be9f/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f2d57696e646f77732d626c75653f7374796c653d666c61742d737175617265266c6f676f3d77696e646f7773266c6f676f436f6c6f723d7768697465" data-canonical-src="https://img.shields.io/badge/-Windows-blue?style=flat-square&amp;logo=windows&amp;logoColor=white" style="max-width: 100%;">
</a>
</p>
声阅是一个PyQt5开发的一款桌面端电子书音频生成应用，用户可以使用它将电子书直接转换成音频，也可以通过Prompt人工指令将电子书用自己的方式重新复述。目前尚未完成，我们将快速部署。希望大家喜欢。

### MacOS 打包

```bash
python build.py \
    --app_name "声阅SonicBooks" \
    --version "0.0.1" \
    --spec_file "main.spec" \
    --entitlements "entitlements.plist" \
    --provisioning_profile "tubev_provision.provisionprofile" \
    --app_certificate "3rd Party Mac Developer Application: John Smith (L42TK32G7A)" \
    --installer_certificate "3rd Party Mac Developer Installer: John Smith (L42TK32G7A)" \
    --output_dir "dist"
```



