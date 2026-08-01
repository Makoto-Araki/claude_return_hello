# claude_return_hello

"Hello" と出力するだけのシンプルなプログラムを、Docker Desktop の Kubernetes 上で CronJob として1時間ごとに実行するサンプルです。

## 構成

```
.
├── src/
│   └── hello.py       # アプリ本体
├── k8s/
│   └── cronjob.yaml    # Kubernetes CronJobマニフェスト
└── Dockerfile
```

## ビルド

Docker Desktop の Kubernetes は同じ Docker デーモンを共有しているため、レジストリへの push は不要です。

```bash
docker build -t claude-return-hello:latest .
```

## デプロイ

```bash
kubectl apply -f k8s/cronjob.yaml
kubectl get cronjob
```

## 動作確認

スケジュール（毎時0分）を待たずに手動実行する場合:

```bash
kubectl create job --from=cronjob/hello-cronjob hello-test
kubectl logs job/hello-test
```
