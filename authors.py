import cleansingAuthors, re

class Author:
    def __init__(self, publications, keywords, fullname='', src=None):
        if fullname != '':
            if re.compile(r'\s\s+').search(fullname):
                fullname = re.compile(r'\s\s+').sub(' ', fullname).strip()
            match = re.compile(r'([A-Z])\s([a-z])').search(fullname)
            if match:
                fullname = re.compile(r'([A-Z])\s([a-z])').sub(match.group(1)+match.group(2), fullname)
            fullname = cleansingAuthors.denoising_name(fullname)
            
        self.fullname = fullname
        self.name_chk_key = self.fullname.replace(' ', '').lower()
        self.name_variants = []
        
        self.wos_auid = None
        self.scp_auid = None
        self.numofmiddlename = Author.how_many_middle_name(self.fullname)
        
        self.src = src
        self.firstname = None
        self.lastname = None        
        self.email = None
        
        self.affiliations = []
        if str(keywords) == 'None' or str(keywords) == 'nan':
            keywords = []
        self.keywords = keywords
        self.publications = publications

    def update_au(self, a,s,w,i):
        if i:
            self.update_info(i, 'ieee')
        if w:
            self.update_info(w, 'wos')
        if a:
            self.update_info(a, 'axv')
        if s:
            self.update_info(s, 'scp')

    def update_info(self, x, src):
        if x.get('daisng_id'):
            self.wos_auid = str(x['daisng_id'])
        if x.get('au_id'):
            self.scp_auid = str(x['au_id'])
        if x.get('firstname'):
            self.firstname = x['firstname']
        if x.get('lastname'):
            self.lastname = x['lastname']
        if x.get('email'):
            self.email = x['email']            
        if x.get('affiliation'):            
            self.affiliations.append(x['affiliation'])
            
    def to_dict(self):
        if self.wos_auid:
            self.wos_auid = str(self.wos_auid)
        if self.scp_auid:
            self.scp_auid = str(self.scp_auid)
            
        dict_ = { 'keywords' : dict(), 'email' : self.email, 'name_chk_key': self.name_chk_key,
            'affiliations' : self.affiliations, 'publications' : self.publications,
            'firstname' : self.firstname, 'lastname' : self.lastname, 'fullname' :self.fullname,
            'wos_auid' : self.wos_auid, 'scp_auid' : self.scp_auid, 'numofmiddlename' : self.numofmiddlename,
            'name_variants' : self.name_variants, 'src' : self.src
           }
        for k in self.keywords:
            dict_['keywords'][k] = 1
        return dict_
    
    @classmethod
    def from_dict(cls, dict_):
        au = Author(dict_['publications'], dict_['keywords'], dict_['fullname'], dict_['src'])
        au.affiliations = dict_['affiliations']
        au.name_chk_key = dict_['name_chk_key']
        au.email = dict_['email']
        au.lastname = dict_['lastname']
        au.firstname = dict_['firstname']
        au.scp_auid = dict_['scp_auid']
        au.numofmiddlename = dict_['numofmiddlename']
        au.wos_auid = dict_['wos_auid']
        au.name_variants = dict_['name_variants']
        
        return au

    @classmethod
    def how_many_middle_name(cls, x):
        if type(x) != str:
            print("hmmn, x is not str", x)
            return 0
        if x =='': return 0        
        match = x.strip().split(' ')
        return len(match) - 2 if len(match) >= 2 else 0