# TubeV-generator

这是一个基于Python的桌面端电子书音频生成应用。用户可以使用该工具生成自己的电子书音频和视频配音。
测试API KEY
```bash
open_ai_key: "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", 
azure_sub: "ad9574a6101a4ac99f743a6e59aed669",
azure_reg: "japanwest"
```

## 打包

### MacOS 打包
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


