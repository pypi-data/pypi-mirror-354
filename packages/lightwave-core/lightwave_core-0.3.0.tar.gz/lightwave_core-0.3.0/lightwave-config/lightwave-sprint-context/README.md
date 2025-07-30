# Lightwave Sprint Context Templates

This directory contains templates for generating sprint context documents using the [Boilerplate](https://github.com/gruntwork-io/boilerplate) tool.

## Prerequisites

1. Install Boilerplate:
   ```bash
   brew install gruntwork-io/tap/boilerplate
   ```
   
   Or download from [GitHub Releases](https://github.com/gruntwork-io/boilerplate/releases)

## Available Templates

### Global Core Sprint Context Template

A template for generating sprint context documents for Lightwave Shared Core development.

#### Usage

```bash
# Navigate to the lightwave-config/lightwave-sprint-context directory
cd lightwave-config/lightwave-sprint-context

# Generate a new sprint context document using the template
boilerplate -template-folder . -input-folder . -non-interactive -var ProjectName=lightwave-shared-core -var SprintName=core-sprint-02 -var SprintGoal="Implement authentication components" -var MinPythonVersion=3.11 -var PackageStructure=true
```

This will generate a new file named `core-sprint-02-context.md` with the specified parameters.

#### Template Variables

| Variable | Description | Default |
|----------|-------------|---------|
| ProjectName | The name of the project | lightwave-shared-core |
| SprintName | The name of the sprint | core-sprint-01 |
| SprintGoal | The main goal for this sprint | Implement foundational shared components |
| MinPythonVersion | Minimum Python version required | 3.11 |
| PackageStructure | Whether to show the package structure section | true |

#### Interactive Mode

You can also run Boilerplate in interactive mode to be prompted for each variable:

```bash
boilerplate -template-folder . -input-folder .
```

## Creating New Templates

1. Create a template YAML file following the structure of `global-core-sprint-template.yaml`
2. Create a corresponding `boilerplate.yml` file for your template
3. Add appropriate variables and templating logic

## Benefits of Using Templates

- **Consistency**: Ensure all sprint context documents follow the same structure
- **Efficiency**: Generate new sprint documents quickly without starting from scratch
- **Customization**: Easily adapt the template to different projects or sprint types
- **Version Control**: Templates can be versioned and improved over time

## Additional Resources

- [Boilerplate Documentation](https://github.com/gruntwork-io/boilerplate#boilerplate)
- [Go Template Syntax](https://pkg.go.dev/text/template) 