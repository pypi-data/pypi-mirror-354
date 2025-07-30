# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue in MCPManager, please report it by emailing security@mcpmanager.dev or by creating a private security advisory on GitHub.

**Please do not report security vulnerabilities through public GitHub issues.**

### What to include in your report

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if you have one)

### Response timeline

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a detailed response within 72 hours indicating next steps
- We will work to resolve critical vulnerabilities within 7 days
- We will keep you informed of our progress throughout the process

## Security Best Practices

When using MCPManager in production:

1. **Container Security**
   - Run MCPManager with minimal privileges
   - Use Docker's user namespace remapping
   - Regularly update base images
   - Scan images for vulnerabilities

2. **Network Security**
   - Configure proper firewall rules
   - Use TLS for all external communications
   - Limit CORS origins to trusted domains
   - Implement network segmentation

3. **Authentication & Authorization**
   - Enable OIDC authentication in production
   - Use Cedar policies for fine-grained authorization
   - Regularly rotate secrets and tokens
   - Monitor authentication logs

4. **Secrets Management**
   - Use encrypted secrets backend or 1Password
   - Never store secrets in environment variables
   - Implement secret rotation policies
   - Use least-privilege principle

5. **Monitoring & Auditing**
   - Enable audit logging
   - Monitor for suspicious activities
   - Set up alerting for security events
   - Regularly review access logs

## Known Security Considerations

1. **Docker Socket Access**: MCPManager requires access to Docker socket. This provides significant privileges and should be carefully managed in production.

2. **Container Privileges**: MCP servers run in containers with configurable permission profiles. Review and customize these profiles based on your security requirements.

3. **API Security**: The REST API should be properly secured with authentication and authorization in production deployments.

## Security Updates

Security updates will be released as patch versions and announced through:
- GitHub Security Advisories
- Release notes
- Security mailing list (when available)

Subscribe to repository notifications to receive security updates.