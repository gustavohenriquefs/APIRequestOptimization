from typing import Dict

MEASUREMENTS = {
    'quilômetros': 'km',
    'metros': 'm',
    'centímetros': 'cm',
    'milímetros': 'mm',
    'quilogramas': 'kg',
    'gramas': 'g',
    'miligramas': 'mg',
    'litros': 'l',
    'mililitros': 'ml',
    'kilometers': 'km',
    'meters': 'm',
    'centimeters': 'cm',
    'millimeters': 'mm',
    'kilograms': 'kg',
    'grams': 'g',
    'milligrams': 'mg',
    'liters': 'l',
    'milliliters': 'ml'
}

TIME_UNITS = {
    'janeiro': 'jan',
    'fevereiro': 'fev',
    'março': 'mar',
    'abril': 'abr',
    'maio': 'mai',
    'junho': 'jun',
    'julho': 'jul',
    'agosto': 'ago',
    'setembro': 'set',
    'outubro': 'out',
    'novembro': 'nov',
    'dezembro': 'dez',
    'january': 'jan',
    'february': 'feb',
    'march': 'mar',
    'april': 'apr',
    'may': 'may',
    'june': 'jun',
    'july': 'jul',
    'august': 'aug',
    'september': 'sep',
    'october': 'oct',
    'november': 'nov',
    'december': 'dec',
    'segunda-feira': 'seg',
    'terça-feira': 'ter',
    'quarta-feira': 'qua',
    'quinta-feira': 'qui',
    'sexta-feira': 'sex',
    'sábado': 'sab',
    'domingo': 'dom',
    'monday': 'mon',
    'tuesday': 'tue',
    'wednesday': 'wed',
    'thursday': 'thu',
    'friday': 'fri',
    'saturday': 'sat',
    'sunday': 'sun'
}

ORGANIZATIONS = {
    'universidade': 'univ',
    'university': 'univ',
    'faculdade': 'fac',
    'college': 'college',
    'empresa': 'emp',
    'company': 'co',
    'corporação': 'corp',
    'corporation': 'corp',
    'organização': 'org',
    'organization': 'org',
    'associação': 'assoc',
    'association': 'assoc',
    'fundação': 'fund',
    'foundation': 'found',
    'instituto': 'inst',
    'institute': 'inst',
    'departamento': 'dept',
    'department': 'dept'
}

TITLES = {
    'senhor': 'sr',
    'senhora': 'sra',
    'doutor': 'dr',
    'doutora': 'dra',
    'professor': 'prof',
    'professora': 'profa',
    'engenheiro': 'eng',
    'engenheira': 'enga',
    'arquiteto': 'arq',
    'arquiteta': 'arqa',
    'mister': 'mr',
    'misses': 'mrs',
    'doctor': 'dr',
    'professor': 'prof',
    'engineer': 'eng',
    'architect': 'arch'
}

BUSINESS_TERMS = {
    'desenvolvimento': 'dev',
    'development': 'dev',
    'aplicação': 'app',
    'application': 'app',
    'sistema': 'sys',
    'system': 'sys',
    'administração': 'admin',
    'administration': 'admin',
    'configuração': 'config',
    'configuration': 'config',
    'informação': 'info',
    'information': 'info',
    'documentação': 'doc',
    'documentation': 'doc',
    'especificação': 'spec',
    'specification': 'spec',
    'implementação': 'impl',
    'tecnologia': 'tech',
    'technology': 'tech',
    'avançada': 'adv',
    'advanced': 'adv',
    'moderno': 'mod',
    'moderna': 'mod',
    'modern': 'mod',
    'software': 'sw',
    'programa': 'prog',
    'program': 'prog',
    'implementation': 'impl'
}

DIRECTIONS = {
    'norte': 'N',
    'sul': 'S',
    'leste': 'L',
    'oeste': 'O',
    'nordeste': 'NE',
    'noroeste': 'NO',
    'sudeste': 'SE',
    'sudoeste': 'SO',
    'north': 'N',
    'south': 'S',
    'east': 'E',
    'west': 'W',
    'northeast': 'NE',
    'northwest': 'NW',
    'southeast': 'SE',
    'southwest': 'SW'
}

def get_all_abbreviations() -> Dict[str, str]:
    all_abbrev = {}
    all_abbrev.update(MEASUREMENTS)
    all_abbrev.update(TIME_UNITS)
    all_abbrev.update(ORGANIZATIONS)
    all_abbrev.update(TITLES)
    all_abbrev.update(BUSINESS_TERMS)
    all_abbrev.update(DIRECTIONS)
    return all_abbrev

def get_savings_potential(text: str) -> Dict[str, int]:
    abbrevs = get_all_abbreviations()
    savings = 0
    opportunities = 0
    
    text_lower = text.lower()
    for original, abbrev in abbrevs.items():
        if original in text_lower:
            count = text_lower.count(original)
            savings += count * (len(original) - len(abbrev))
            opportunities += count
    
    return {
        'total_savings': savings,
        'opportunities': opportunities,
        'current_length': len(text)
    }
