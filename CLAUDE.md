# claude_return_hello

"Hello" を出力するだけの最小プログラムを、ローカル Docker Desktop の Kubernetes 上で CronJob として1時間ごとに実行する検証用リポジトリ。

## 構成
- `src/hello.py` — アプリ本体
- `tests/test_hello.py` — `hello.py` のテスト
- `requirements-dev.txt` — テスト実行用の開発依存（pytest のみ）
- `k8s/cronjob.yaml` — CronJob マニフェスト
- `Dockerfile` — ルート直下に配置（`docker build .` やCI/CDが既定でルートのDockerfileを探すため）
- `.github/workflows/` — CI/CD ワークフロー（PRテスト・mainマージ時のテスト+脆弱性スキャン・タグpush時のDocker Hubリリース）
- `.devcontainer/devcontainer.json` — Claude Code での開発用devcontainer定義

## 設計判断
- **`imagePullPolicy: Never`**: Docker Desktop の Kubernetes はホストの Docker デーモンをそのまま共有するため、イメージレジストリへの push は不要。ローカルで `docker build` したイメージをそのまま参照できる。
- **スケジュール `0 * * * *`**: 1時間ごと（毎時0分）に実行する要件のため。
- **Dockerfile はルート直下、ソースは `src/` に分離**: 将来ソースが増えても `src/` 配下に追加していけばよく、Dockerfileの探索場所は慣習通りに保つ。
- **テストは `subprocess` で `hello.py` をスクリプトとして実行し、標準出力を検証**: `main()` への切り出しなどのリファクタリングは行わない。`hello.py` は「2行だけ」であることが設計意図であり、Dockerfile の `CMD ["python", "hello.py"]` や CronJob が実際に叩く経路（スクリプト実行）とテスト内容を一致させるため。
- **開発用依存は `requirements-dev.txt` に pytest のみ**: 既存の依存管理ファイルが元々ない状態に合わせ、`pyproject.toml` のようなパッケージング前提の重い構成は導入しない。
- **ベースイメージは `python:3.12-alpine`**: 当初 `python:3.12-slim`（Debian）を使用していたが、`main-ci.yml` の Trivy スキャンで `perl-base` パッケージの CRITICAL 脆弱性が検出されたため切り替えた。Alpine系には perl-base が含まれず、イメージサイズも小さい。`hello.py` は stdlib のみで動作するため互換性の問題はない。

## 開発フロー
このリポジトリでの変更は、Claude Code を使った以下の手順を標準とする（検証中の手順）。

```
Issue起票 → ブランチ作成 → 実装 → ローカルで動作確認 → PR作成 → レビュー → マージ
```

- GitHub Actions による CI/CD を導入している（詳細は下記「CI/CD」を参照）。Issue/PR テンプレートは、個人の検証用リポジトリの規模に見合わないため引き続き導入しない。
- push・PR作成・マージなど、リモートやmainに影響する操作は、実行前にユーザーの確認を取ってから行う。

## CI/CD
GitHub Actions で以下の3つのワークフローを実行する（`.github/workflows/`）。

- **`pr-test.yml`**（PR作成・更新時、`pull_request` targeting `main`）: pytest を実行する。
- **`main-ci.yml`**（mainへのマージ時、`push` to `main`）: pytest を実行した後、ビルドしたDockerイメージに対して Trivy で脆弱性スキャンを行う。CRITICALのみジョブを失敗させ、HIGH以下はレポートのみ（失敗させない）。
- **`release.yml`**（タグpush時、`push: tags: ['v*']`。GitHubの `release` イベントではなくタグpushをトリガーに使う）: pytest を実行した後、Dockerイメージをビルドし、Docker Hub（`makotoaraki346/claude-return-hello`）に push する。イメージタグは git タグ名をそのまま使用（例: `v1.0.0`。`v` は取り除かない）と `latest` の2つ。

- 3ワークフローで共通するテスト実行手順（checkout → setup-python 3.12 → `pip install -r requirements-dev.txt` → `pytest -q`）は、reusable workflow化せずそのまま重複させている。ワークフローが3つ・テストファイルが1つのみという規模では、reusable workflow による抽象化は複雑さに見合わないため。
- Docker Hub への認証情報は GitHub Actions の Secrets（`DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN`）として登録する。`DOCKERHUB_TOKEN` はDocker Hubのアクセストークン（アカウントパスワードではない）を使う。

## よく使うコマンド
```bash
# ビルド
docker build -t claude-return-hello:latest .

# 適用
kubectl apply -f k8s/cronjob.yaml

# 手動トリガーで即時確認
kubectl create job --from=cronjob/hello-cronjob hello-test
kubectl logs job/hello-test

# テスト
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```
