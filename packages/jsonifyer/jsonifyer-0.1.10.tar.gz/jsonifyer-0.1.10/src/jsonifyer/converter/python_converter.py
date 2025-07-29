import os
import json
import csv
import re
import logging
import xml.etree.ElementTree as ET
from glob import glob
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
from .xslt_converter import apply_xslt_to_xml

logger = logging.getLogger(__name__)

def set_nested_value(d, keys, value):
    for k in keys[:-1]:
        if k.endswith('[]'):
            k = k[:-2]
            d = d.setdefault(k, [])
            if not d or not isinstance(d[-1], dict):
                d.append({})
            d = d[-1]
        else:
            d = d.setdefault(k, {})
    if keys[-1].endswith('[]'):
        k = keys[-1][:-2]
        d.setdefault(k, []).append(value)
    else:
        d[keys[-1]] = value

def parse_xml_to_json(
    xml_file: str,
    repeated_file: str = None,
    field_map: Optional[Dict[str, str]] = None,
    fields: Optional[List[str]] = None,
    namespaces: Optional[Dict[str, str]] = None,
    root_tag: Optional[str] = None,
    extra_fields: Optional[Dict[str, str]] = None,
    pairs: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:

    tree = ET.parse(xml_file)
    root = tree.getroot()
    default_ns = root.tag.split('}')[0].strip('{') if '}' in root.tag else None
    
    ns_prefix = 'ns'
    extra_ns = namespaces
    if default_ns:
        namespaces = {ns_prefix: default_ns}
        
    def add_prefix(xpath):
        if default_ns:
            parts = xpath.split('/')
            new_parts = []
            for part in parts:
                if part and not part.startswith('.') and not part.startswith('@') and ':' not in part:
                    if part.startswith('*'):
                        new_parts.append(part)
                    else:
                        new_parts.append(f'{ns_prefix}:{part}')
                else:
                    new_parts.append(part)
            return '/'.join(new_parts)
        return xpath
    
    if root_tag:
        root_local = root.tag.split('}')[-1] if '}' in root.tag else root.tag
        if root_local.strip().lower() != root_tag.strip().lower():
            if default_ns:
                root = root.find(f'.//{{{default_ns}}}{root_tag.strip()}')
            else:
                root = root.find(f'.//{root_tag.strip()}')
            if root is None:
                return {}
    
    def safe_find(element, xpath):
        try:
            xpath = add_prefix(xpath)
            if not xpath.startswith('.') and not xpath.startswith('/'):
                xpath = './' + xpath
            result = element.find(xpath, namespaces)
            return result
        except Exception as e:
            return None
    
    def safe_findall(element, xpath):
        try:
            xpath = add_prefix(xpath)
            if not xpath.startswith('.') and not xpath.startswith('/'):
                xpath = './' + xpath
            lst = element.findall(xpath, namespaces)
            lst_to_compare = [el.text.strip() for el in lst]
            if all(txt == lst_to_compare[0] for txt in lst_to_compare):
                lst = lst[0]
            else:
                s = set()
                lst_to_ret = []
                for el in lst:
                    if el.text.strip() not in s:
                        s.add(el.text.strip())
                        lst_to_ret.append(el)
                lst = lst_to_ret
            return lst
        except Exception as e:
            print("BATATOLAS" + str(e))
            return []
    
    def extract_element_data(element):
        if element is None:
            return None
            
        result = {}
        
        for key, value in element.attrib.items():
            result[key] = value
            
        if element.text and element.text.strip():
            result['text'] = element.text.strip()
            
        for child in element:
            child_data = extract_element_data(child)
            if child_data:
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if tag in result:
                    if not isinstance(result[tag], list):
                        result[tag] = [result[tag]]
                    result[tag].append(child_data)
                else:
                    result[tag] = child_data
                    
        return result

    def extract_section_text(code_value):
        for section in root.findall('.//section', extra_ns):
            code = section.find('code', extra_ns)
            if code is not None and code.attrib.get('code') == code_value:
                text_elem = section.find('text', extra_ns)
                if text_elem is not None and ''.join(text_elem.itertext()).strip():
                    return ''.join(text_elem.itertext()).strip()
                excerpt_elem = section.find('excerpt', extra_ns)
                if excerpt_elem is not None:
                    return ' '.join([t.strip() for t in excerpt_elem.itertext() if t.strip()])
        return None
    
    result = {}
    
    if field_map:
        for field, xpath in field_map.items():
            if isinstance(xpath, list):
                values = []
                for path in xpath:
                    elements = safe_findall(root, path)
                    for element in elements:
                        if element is not None and element.text:
                            values.append(element.text.strip())
                
                if values:
                    if '.' in field:
                        parts = field.split('.')
                        current = result
                        for part in parts[:-1]:
                            if part not in current:
                                current[part] = {}
                            current = current[part]
                        current[parts[-1]] = values
                    else:
                        result[field] = values
            elif '@' in xpath:
                base_path, attr = xpath.rsplit('@', 1)
                base_path = base_path.rstrip('/').strip()
                attr = attr.strip()
                element = safe_find(root, base_path)

                if element is not None and attr in element.attrib:
                    if '.' in field:
                        tag = field.split('.')[0]
                        tagg = field.split('.')[-1]
                        if isinstance(element, list):
                            result[tag] = []
                            for el in element:
                                if isinstance(el, ET.Element):
                                    result[tag].append({str(tagg): el.text.strip() if el.text else None})
                                else:
                                    result[tag].append({str(tagg): el})
                    else:
                        result[field] = element.attrib[attr]
            else:
                element = safe_findall(root, xpath)
                if element is not None:
                    if '.' in field:
                        tag = field.split('.')[0]
                        tagg = field.split('.')[-1]
                        if isinstance(element, list):
                            result[tag] = []
                            for el in element:
                                if isinstance(el, ET.Element):
                                    result[tag].append({str(tagg): el.text.strip() if el.text else None})
                                else:
                                    result[tag].append({str(tagg): el})
                    else:
                        tag = xpath.split('/')[-1]
                        if isinstance(element, list):
                            result[field] = []
                            for el in element:
                                result[field].append({str(tag): el.text.strip() if el.text else None})
                        else:
                            result[field] = element.text.strip() if element.text else None
            
            if extra_fields:
                for field_name, code_value in extra_fields.items():
                    section_text = extract_section_text(code_value)
                    if section_text:
                        result[field_name] = section_text

            if pairs:
                tag = list(pairs.keys())[0].split(".")[0]
                tagg = [pr.split(".")[-1] for pr in list(pairs.keys())]
                result[tag] = []
                for xpquery in pairs.values():
                    generic_elem = root.findall(xpquery[0], extra_ns)
                    for sub in generic_elem:
                        dict_to_append = {}
                        for alpha_i, alpha in enumerate([x[-1] for x in list(pairs.values())]):
                            if len(alpha.split("/")) == 1:
                                dict_to_append[tagg[alpha_i]] = ''.join(sub.find(alpha, extra_ns).itertext()).strip() if sub.find(alpha, extra_ns) is not None else None
                            else:
                                to_search = alpha.split("/")
                                dict_to_append[tagg[alpha_i]] = sub.find(to_search[0], extra_ns).attrib.get(to_search[1][1:]) if sub.find(to_search[0], extra_ns) is not None else None
                        result[tag].append(dict_to_append)
                s = set()
                lst_to_ret = []
                for el in result[tag]:
                    if el[tagg[0]] not in s:
                        s.add(el[tagg[0]])
                        lst_to_ret.append(el)
                result[tag] = lst_to_ret

    elif fields:
        for xpath in fields:
            if '@' in xpath:
                base_path, attr = xpath.rsplit('@', 1)
                base_path = base_path.rstrip('/').strip()
                attr = attr.strip()
                element = safe_find(root, base_path)
                if element is not None and attr in element.attrib:
                    result[attr] = element.attrib[attr]
            else:
                element = safe_find(root, xpath)
                if element is not None:
                    tag = xpath.split('/')[-1]
                    if len(element) > 0:
                        result[tag] = extract_element_data(element)
                    else:
                        result[tag] = element.text.strip() if element.text else None
    
    else:
        result = extract_element_data(root)
    
    return result

def convert_csv(

    input_file: str,
    output_dir: str,
    skiprows: int = 0,
    field_map: Optional[Dict[str, int]] = None
) -> List[str]:

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    created_files = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for _ in range(skiprows):
            next(reader)
        
        for i, row in enumerate(reader):
            if not row or not any(row):  
                continue
                
            record = {}
            if field_map:
                for field_name, col_idx in field_map.items():
                    if col_idx < len(row):
                        value = row[col_idx].strip()
                        if value:  
                            record[field_name] = value
            else:
                record = {f"column_{i}": value.strip() for i, value in enumerate(row) if value.strip()}
            
            if record and len(record) > 1:  
                output_file = output_path / f"record_{i+1}.json"
                with open(output_file, 'w', encoding='utf-8') as out_f:
                    json.dump(record, out_f, indent=4, ensure_ascii=False)
                created_files.append(str(output_file))
    
    print(f"Created {len(created_files)} JSON files in {output_dir}")
    return created_files



def check_null_fields(json_data: Dict) -> List[str]:
    null_fields = []
    
    def recursive_check(data: Any, parent_key: str = "") -> None:
        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if value is None:
                    null_fields.append(full_key)
                else:
                    recursive_check(value, full_key)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                recursive_check(item, f"{parent_key}[{index}]")
    recursive_check(json_data)
    return null_fields



class PythonConverter:
    def convert_xml_structured(self, input_file: str, output_dir: str, field_map: Dict[str, str], namespaces: Optional[Dict[str, str]] = None) -> None:
        result = parse_xml_to_json(input_file, field_map=field_map, namespaces=namespaces)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + '.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4, ensure_ascii=False)