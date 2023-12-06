# TubeV-generator

这是一个基于Python的桌面端电子书音频生成应用

## 打包
### MacOS 桌面版
```bash
python build.py \
    --app_name "Tubev" \
    --version "0.0.1" \
    --spec_file "main.spec" \
    --entitlements "entitlements.plist" \
    --provisioning_profile "tubev_provision.provisionprofile" \
    --app_certificate "3rd Party Mac Developer Application: John Smith (L42TK32G7A)" \
    --installer_certificate "3rd Party Mac Developer Installer: John Smith (L42TK32G7A)" \
    --output_dir "dist"
```


### Windows 桌面版
