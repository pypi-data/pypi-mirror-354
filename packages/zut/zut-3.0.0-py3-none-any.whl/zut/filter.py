from __future__ import annotations
import re
from zut import slugify


class Filter:
    def __init__(self, spec: str|re.Pattern, *, normalize: bool = False):
        self.normalize = normalize

        if isinstance(spec, re.Pattern):
            self.spec = spec

        elif isinstance(spec, str) and spec.startswith('^'):
            m = re.match(r'^(.*\$)(A|I|L|U|M|S|X)+$', spec, re.IGNORECASE)
            if m:
                pattern = m[1]
                flags = re.NOFLAG
                for letter in m[2]:
                    flags |= re.RegexFlag[letter.upper()]
            else:
                pattern = spec
                flags = re.NOFLAG

            self.spec = re.compile(pattern, flags)

        elif isinstance(spec, str):
            if self.normalize:
                spec = self.normalize_spec(spec)

            if '*' in spec:
                name_parts = spec.split('*')
                pattern_parts = [re.escape(name_part) for name_part in name_parts]
                pattern = r'^' + r'.*'.join(pattern_parts) + r'$'
                self.spec = re.compile(pattern)
            else:
                self.spec = spec

        else:
            raise TypeError(f"Filter spec must be a string or regex pattern, got {type(spec).__name__}")
       

    def __repr__(self) -> str:
        return self.spec.pattern if isinstance(self.spec, re.Pattern) else self.spec


    def matches(self, value: str, is_normalized: bool = False):
        if value is None:
            value = ""
        elif not isinstance(value, str):
            value = str(value)

        if self.normalize and not is_normalized:
            value = self.normalize_value(value)

        if isinstance(self.spec, re.Pattern):
            if self.spec.match(value):
                return True
            
        elif self.spec == value:
            return True


    @classmethod
    def normalize_spec(cls, spec: str):
        return slugify(spec, separator=None, keep='*', strip_keep=False, if_none=None)
    
    
    @classmethod
    def normalize_value(cls, value: str):
        return slugify(value, separator=None, keep=None, if_none=None)


class Filters:
    def __init__(self, specs: list[str|re.Pattern]|str|re.Pattern, *, normalize: bool = False):
        self.filters: list[Filter] = []

        if specs:
            if isinstance(specs, (str,re.Pattern)):
                specs = [specs]

            for spec in specs:
                self.filters.append(Filter(spec, normalize=normalize))


    def __len__(self):
        return len(self.filters)


    def matches(self, value: str, if_no_filter: bool = False):
        if not self.filters:
            return if_no_filter
        
        if value is None:
            value = ""
        elif not isinstance(value, str):
            value = str(value)
        
        normalized_value = None    

        for str_filter in self.filters:
            if str_filter.normalize:
                if normalized_value is None:
                    normalized_value = Filter.normalize_value(value)
                if str_filter.matches(normalized_value, is_normalized=True):
                    return True
            else:
                if str_filter.matches(value):
                    return True
                
        return False
