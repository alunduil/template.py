# Sharing Git credentials with your container

Visual Studio Code devcontainers supports using your local Git configuration from inside a container.

If this is set-up incorrectly you'll still be able to use devcontainers, but you'll need to add your Git credentials in each devcontainer.

Your set-up will depend on whether you use HTTPS or SSH to connect with Github:

1. If you're using HTTPS, you need to configure a credential helper in your local OS
1. If you're using SSH your local keys need to be added in the SSH agent

[See how to set-up your Git credentials for devcontainers here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
