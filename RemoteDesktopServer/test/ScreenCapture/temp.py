import pefile

# 解析するDLLのパス
dll_path = "./ScreenCapture.dll"

# DLLファイルを読み込む
pe = pefile.PE(dll_path)

# エクスポートされている関数を表示
if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
    for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        print(f"{hex(pe.OPTIONAL_HEADER.ImageBase + exp.address)}: {exp.name.decode('utf-8')}")
else:
    print("エクスポートされている関数が見つかりませんでした。")