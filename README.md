# NikkouServerBOT

## 環境構築

> [!WARNING]
> python3 がインストールされている前提です。

### クローン

GitHub からリポジトリをクローンします。

```bash
git clone https://github.com/nikkou-0814/NikkouServerBOT
```

### 環境変数

1. .env.example をコピーします。

```bash
cp .env.example .env
```

Discord BOT のトークンを記載します。

3. TOKEN=<DISOCRD_TOKEN>。

## 依存関係のインストールと起動

依存関係の管理は Poetry を使用しています。

```bash
poetry env use <which python>
poetry install
poetry run python bot.py
```

## 注意

この BOT は NikkouServer 専用に最適化されているので、コードを使用して他のサーバーに導入することを、我々は推奨しておりません。

## 開発者へ

gitmoji の使用を開始したので、できれば gitmoji でのコミットをしてください。

https://marketplace.visualstudio.com/items?itemName=seatonjiang.gitmoji-vscode
