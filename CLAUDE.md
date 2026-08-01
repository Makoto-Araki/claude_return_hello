# claude_return_hello

"Hello" を出力するだけの最小プログラムを、ローカル Docker Desktop の Kubernetes 上で CronJob として1時間ごとに実行する検証用リポジトリ。

## 構成
- `src/hello.py` — アプリ本体
- `k8s/cronjob.yaml` — CronJob マニフェスト
- `Dockerfile` — ルート直下に配置（`docker build .` やCI/CDが既定でルートのDockerfileを探すため）

## 設計判断
- **`imagePullPolicy: Never`**: Docker Desktop の Kubernetes はホストの Docker デーモンをそのまま共有するため、イメージレジストリへの push は不要。ローカルで `docker build` したイメージをそのまま参照できる。
- **スケジュール `0 * * * *`**: 1時間ごと（毎時0分）に実行する要件のため。
- **Dockerfile はルート直下、ソースは `src/` に分離**: 将来ソースが増えても `src/` 配下に追加していけばよく、Dockerfileの探索場所は慣習通りに保つ。

## よく使うコマンド
```bash
# ビルド
docker build -t claude-return-hello:latest .

# 適用
kubectl apply -f k8s/cronjob.yaml

# 手動トリガーで即時確認
kubectl create job --from=cronjob/hello-cronjob hello-test
kubectl logs job/hello-test
```
