.PHONY: help install dev test lint format check clean run

help: ## 显示帮助
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## 安装依赖
	pip install -r requirements.txt

dev: ## 安装开发依赖
	pip install -r requirements.txt
	pip install -e ".[dev]"

test: ## 运行测试
	pytest

test-cov: ## 运行测试并显示覆盖率
	pytest --cov=src --cov-report=html
	@echo "覆盖率报告已生成: htmlcov/index.html"

lint: ## 运行代码检查
	ruff check src/ main.py

format: ## 格式化代码
	ruff format src/ main.py
	ruff check src/ main.py --fix

check: ## 运行所有检查（lint + test）
	ruff check src/ main.py
	pytest

type-check: ## 运行类型检查
	mypy src/ main.py

clean: ## 清理临时文件
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ .pytest_cache/ .mypy_cache/ htmlcov/ .coverage

run: ## 运行程序
	python main.py

docker-build: ## 构建Docker镜像
	docker build -t wxauto-onebot .

docker-run: ## 运行Docker容器
	docker run -p 10001:10001 -v ./config:/app/config wxauto-onebot

setup-git: ## 设置Git钩子
	pip install pre-commit
	pre-commit install
	@echo "Git钩子已安装"
