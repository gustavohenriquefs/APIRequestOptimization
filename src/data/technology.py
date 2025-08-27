"""
Termos técnicos e tecnológicos para preservação e abreviação.
"""
from typing import Dict, List

# Tecnologias e linguagens de programação
PROGRAMMING_TECHNOLOGIES = {
    'JavaScript': 'JS',
    'TypeScript': 'TS',
    'Python': 'Py',
    'Java': 'Java',
    'C Sharp': 'C#',
    'C++': 'C++',
    'PHP': 'PHP',
    'Ruby': 'Ruby',
    'Go': 'Go',
    'Rust': 'Rust',
    'Swift': 'Swift',
    'Kotlin': 'Kt',
    'Scala': 'Scala',
    'R': 'R'
}

# Frameworks e bibliotecas
FRAMEWORKS = {
    'React': 'React',
    'Angular': 'Angular',
    'Vue.js': 'Vue',
    'Next.js': 'Next',
    'Express.js': 'Express',
    'Django': 'Django',
    'Flask': 'Flask',
    'Spring Boot': 'Spring',
    'Laravel': 'Laravel',
    'Ruby on Rails': 'Rails',
    'ASP.NET': 'ASP',
    'Node.js': 'Node'
}

# Banco de dados
DATABASES = {
    'MySQL': 'MySQL',
    'PostgreSQL': 'PG',
    'MongoDB': 'Mongo',
    'Redis': 'Redis',
    'SQLite': 'SQLite',
    'Oracle Database': 'Oracle',
    'Microsoft SQL Server': 'MSSQL',
    'Elasticsearch': 'ES',
    'Cassandra': 'Cassandra'
}

# Cloud e DevOps
CLOUD_DEVOPS = {
    'Amazon Web Services': 'AWS',
    'Microsoft Azure': 'Azure',
    'Google Cloud Platform': 'GCP',
    'Docker': 'Docker',
    'Kubernetes': 'K8s',
    'Jenkins': 'Jenkins',
    'GitLab': 'GitLab',
    'GitHub': 'GitHub',
    'Terraform': 'TF',
    'Ansible': 'Ansible'
}

# Protocolos e APIs
PROTOCOLS_APIS = {
    'Application Programming Interface': 'API',
    'Hypertext Transfer Protocol': 'HTTP',
    'HTTP Secure': 'HTTPS',
    'File Transfer Protocol': 'FTP',
    'Simple Mail Transfer Protocol': 'SMTP',
    'Transmission Control Protocol': 'TCP',
    'User Datagram Protocol': 'UDP',
    'Internet Protocol': 'IP',
    'Domain Name System': 'DNS',
    'Secure Shell': 'SSH'
}

# Formatos de dados
DATA_FORMATS = {
    'JavaScript Object Notation': 'JSON',
    'Extensible Markup Language': 'XML',
    'YAML Ain\'t Markup Language': 'YAML',
    'Comma-Separated Values': 'CSV',
    'Portable Document Format': 'PDF',
    'HyperText Markup Language': 'HTML',
    'Cascading Style Sheets': 'CSS'
}

# Inteligência Artificial e ML
AI_ML_TERMS = {
    'Inteligência Artificial': 'IA',
    'Artificial Intelligence': 'AI',
    'Machine Learning': 'ML',
    'Deep Learning': 'DL',
    'Neural Network': 'NN',
    'Natural Language Processing': 'NLP',
    'Processamento de Linguagem Natural': 'PLN',
    'Computer Vision': 'CV',
    'Large Language Model': 'LLM',
    'Generative Pre-trained Transformer': 'GPT',
    'Convolutional Neural Network': 'CNN',
    'Recurrent Neural Network': 'RNN'
}

# Metodologias e processos
METHODOLOGIES = {
    'Agile': 'Agile',
    'Scrum': 'Scrum',
    'DevOps': 'DevOps',
    'Continuous Integration': 'CI',
    'Continuous Deployment': 'CD',
    'Test Driven Development': 'TDD',
    'Behavior Driven Development': 'BDD',
    'Model View Controller': 'MVC',
    'Model View ViewModel': 'MVVM',
    'Representational State Transfer': 'REST',
    'GraphQL': 'GraphQL'
}

def get_all_tech_terms() -> Dict[str, str]:
    """Retorna todos os termos técnicos."""
    all_tech = {}
    all_tech.update(PROGRAMMING_TECHNOLOGIES)
    all_tech.update(FRAMEWORKS)
    all_tech.update(DATABASES)
    all_tech.update(CLOUD_DEVOPS)
    all_tech.update(PROTOCOLS_APIS)
    all_tech.update(DATA_FORMATS)
    all_tech.update(AI_ML_TERMS)
    all_tech.update(METHODOLOGIES)
    return all_tech

def is_tech_term(text: str) -> bool:
    """Verifica se o texto é um termo técnico."""
    tech_terms = get_all_tech_terms()
    return text in tech_terms or text in tech_terms.values()

# Categorias de preservação para termos técnicos
TECH_PRESERVATION = {
    'never_compress': {'API', 'HTTP', 'HTTPS', 'JSON', 'XML', 'SQL', 'HTML', 'CSS'},
    'minimal_compress': set(AI_ML_TERMS.values()) | set(PROTOCOLS_APIS.values()),
    'moderate_compress': set(FRAMEWORKS.values()) | set(DATABASES.values()),
    'can_compress': set(METHODOLOGIES.values())
}
