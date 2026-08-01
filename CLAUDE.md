# claude_return_hello

"Hello" を出力するだけの最小プログラムを、ローカル Docker Desktop の Kubernetes 上で CronJob として1時間ごとに実行する検証用リポジトリ。

## 構成
- `src/hello.py` — アプリ本体
- `tests/test_hello.py` — `hello.py` のテスト
- `requirements-dev.txt` — テスト実行用の開発依存（pytest のみ）
- `k8s/cronjob.yaml` — CronJob マニフェスト
- `Dockerfile` — ルート直下に配置（`docker build .` やCI/CDが既定でルートのDockerfileを探すため）

## 設計判断
- **`imagePullPolicy: Never`**: Docker Desktop の Kubernetes はホストの Docker デーモンをそのまま共有するため、イメージレジストリへの push は不要。ローカルで `docker build` したイメージをそのまま参照できる。
- **スケジュール `0 * * * *`**: 1時間ごと（毎時0分）に実行する要件のため。
- **Dockerfile はルート直下、ソースは `src/` に分離**: 将来ソースが増えても `src/` 配下に追加していけばよく、Dockerfileの探索場所は慣習通りに保つ。
- **テストは `subprocess` で `hello.py` をスクリプトとして実行し、標準出力を検証**: `main()` への切り出しなどのリファクタリングは行わない。`hello.py` は「2行だけ」であることが設計意図であり、Dockerfile の `CMD ["python", "hello.py"]` や CronJob が実際に叩く経路（スクリプト実行）とテスト内容を一致させるため。
- **開発用依存は `requirements-dev.txt` に pytest のみ**: 既存の依存管理ファイルが元々ない状態に合わせ、`pyproject.toml` のようなパッケージング前提の重い構成は導入しない。

## 開発フロー
このリポジトリでの変更は、Claude Code を使った以下の手順を標準とする（検証中の手順）。

```
Issue起票 → ブランチ作成 → 実装 → ローカルで動作確認 → PR作成 → レビュー → マージ
```

- 個人の検証用リポジトリのため、CI/CD（GitHub Actions）や Issue/PR テンプレートは導入しない。プロセスは規模に見合った最小限にとどめる。
- push・PR作成・マージなど、リモートやmainに影響する操作は、実行前にユーザーの確認を取ってから行う。

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
