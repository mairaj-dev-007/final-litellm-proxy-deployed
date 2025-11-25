FROM ghcr.io/berriai/litellm:main-stable

# Copy custom middleware and config
COPY custom_proxy.py /app/custom_proxy.py
COPY proxy.py /app/proxy.py
COPY config.yaml /app/config.yaml

# Set working directory
WORKDIR /app

# Expose the default LiteLLM port
EXPOSE 4000

# Override the entrypoint and use uvicorn directly
ENTRYPOINT []
CMD ["python", "-m", "uvicorn", "custom_proxy:app", "--host", "0.0.0.0", "--port", "4000"]
