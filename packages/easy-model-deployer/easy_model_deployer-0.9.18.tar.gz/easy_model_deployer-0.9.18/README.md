<p align="center">
    <h3 align="center">Easy Model Deployer: Simple, Efficient, and Easy-to-Integrate</h3>
</p>

<p align="center">
  <a href="https://aws-samples.github.io/easy-model-deployer/en/installation"><strong>Documentation</strong></a> ·
  <a href="https://github.com/aws-samples/easy-model-deployer/releases"><strong>Changelog</strong></a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellowgreen.svg" alt="MIT License"></a>
  <a href="https://pypi.org/project/easy_model_deployer"><img src="https://img.shields.io/pypi/v/easy_model_deployer.svg?logo=pypi&label=PyPI&logoColor=gold"></a>
  <a href="https://pypi.org/project/easy_model_deployer"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/easy-model-deployer"></a>
  <a href="https://github.com/aws-samples/easy-model-deployer/actions/workflows/release-package.yml"><img src="https://github.com/aws-samples/easy-model-deployer/actions/workflows/release-package.yml/badge.svg" alt="Build Status"></a>
</p>

## 🔥 Latest News
- 2025-04-29: Deploy Qwen 3 series models with [one command line](https://github.com/aws-samples/easy-model-deployer/blob/main/docs/en/best_deployment_practices.md##famous-models###Qwen-3-Series).
- 2025-04-21: Deploy GLM Z1/0414 series models with [one command line](https://github.com/aws-samples/easy-model-deployer/blob/main/docs/en/best_deployment_practices.md##famous-models###GLM-Z1/0414-Series).
- 2025-03-17: Deploy Gemma 3 series models with [one command line](https://github.com/aws-samples/easy-model-deployer/blob/main/docs/en/best_deployment_practices.md##famous-models###gemma-3-series).
- 2025-03-06: Deploy QwQ-32B with [one command line](docs/en/best_deployment_practices.md##famous-models###qwen-series###qwq-32b).

## Introduction

Easy Model Deployer is a lightweight tool designed for simplify deploy **Open-Source LLMs** ([Supported Models](docs/en/supported_models.md)) and Custom Models on AWS. It provides **OpenAI's Completions API** and [**LangChain Interface**](https://github.com/langchain-ai/langchain). Built for developers who need reliable and scalable model serving without complex environment setup.

![cli](docs/images/demo.avif)

**Key Features**

- One-click deployment of models to AWS (Amazon SageMaker, Amazon ECS, Amazon EC2)
- Diverse model types (LLMs, VLMs, Embeddings, Vision, etc.)
- Rich inference engine (vLLM, TGI, Lmdeploy, etc.)
- Different instance types (CPU/GPU/AWS Inferentia)
- Convenient integration (OpenAI Compatible API, LangChain client, etc.)

## Support Models
<details>
<summary>Deepseek Reasoning Model</summary>
  <a href="https://github.com/deepseek-ai/DeepSeek-R1"><strong>DeepSeek-R1-Distill-Qwen-14B</strong></a>

</details>

## 🔧 Get Started

### Installation

Install Easy Model Deployer with PyPI, currently support for Python 3.9 or above:

```bash
pip install easy-model-deployer
emd
```

### Bootstrap

Prepare the essential resources required for model deployment.

For more information, please refer to [Architecture](https://aws-samples.github.io/easy-model-deployer/en/architecture/).

```bash
emd bootstrap
```

> **💡 Tip** Once you upgrade the EMD by `pip`, you need to run this command again to update the environment.

### Deploy Models

Deploy models with an interactive CLI or one command line.

```bash
emd deploy
```

> **💡 Tip** To view all available parameters, run `emd deploy --help`.
> When you see the message "Waiting for model: ...", it means the deployment task has started and you can stop the terminal output by pressing `Ctrl+C`.
>
> - For more information on deployment parameters, please refer to the [Deployment parameters](docs/en/installation.md).
> - For best practice examples of using command line parameters, please refer to the [Best Deployment Practices](docs/en/best_deployment_practices.md).

### Show Status

Check the status of the model deployment task.

```bash
emd status
```

> **💡 Tip** The EMD allows launch multiple deployment tasks simultaneously.

### Invocation

Invoke the deployed model for testing by CLI.

```bash
emd invoke DeepSeek-R1-Distill-Qwen-1.5B
```

> **💡 Tip** You can find the *ModelId* in the output by `emd status`.

- [Integration examples](https://aws-samples.github.io/easy-model-deployer/)
- [EMD client](docs/en/emd_client.md)
- [Langchain interface](docs/en/langchain_interface.md)
- [OpenAI compatible interface](docs/en/openai_compatiable.md).

> **💡 Tip** OpenAI Compatible API is supported only for Amazon ECS and Amazon EC2 deployment types.

### List Supported Models

Quickly see what models are supported, this command will output all information related to deployment. (Plese browse [Supported Models](docs/en/supported_models.md) for more information.)

```bash
emd list-supported-models
```


### Delete Model

Delete the deployed model.

```bash
emd destroy DeepSeek-R1-Distill-Qwen-1.5B
```

> **💡 Tip** You can find the *ModelId* in the output by `emd status`.

## 📖 Documentation

For advanced configurations and detailed guides, visit our [documentation site](https://aws-samples.github.io/easy-model-deployer/).

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
