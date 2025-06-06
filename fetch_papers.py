import urllib, urllib.request
import pandas as pd

def fetch_recent_cv_papers(keywords, max_result=100):
    
    query = ''.join(['all:'+word+'+AND+' for word in keywords])[:-5]

    url = f'http://export.arxiv.org/api/query?search_query={query}&start=0&max_results={max_result}&sortBy=submittedDate&sortOrder=descending'
    search_result = urllib.request.urlopen(url)
    search_result = search_result.read().decode('utf-8')

    data_list = search_result.split('<entry>\n')
    head = data_list.pop(0)
    
    paper_list = list()

    for data in data_list:
        paper_dict = {}
        paper = data.split('\n')
    
        _id = paper[0].split('<id>')[1].replace('</id>', '')
        
        paper_dict['id'] = _id
        
        # Add published date and title of the paper
        paper_dict['date'] = paper[2].split('<published>')[1].replace('</published>', '')
        # paper_dict['title'] = paper[3].split('<title>')[1].replace('</title>', '')
    
        title = False
        title_text = ''
        
        abstract = False
        abstract_text = ''
        
        author = False
        author_list = list()
        
        # Add abstract and authors of the paper
        for line in paper[3:]:
            if ('<title>' in line) & ('</title>' in line):
                line = line.split('<title>')[1]
                title_text = line.replace('<title>', '').replace('</title>', '').strip()
                paper_dict['title'] = title_text
            elif '<title>' in line:
                title = True
                line = line.split('<title>')[1]
            elif '</title>' in line:
                title_text += line.replace('</title>', '').strip()
                paper_dict['title'] = title_text
                title = False
            if title:
                title_text += line.strip()
                title_text += ' '
        
            if '<summary>' in line:
                abstract = True
                line = line.split(' <summary>')[1]
            elif '</summary>' in line:
                abstract = False
                paper_dict['abstract'] = abstract_text[:-1]
            if abstract:
                abstract_text += line.strip()
                abstract_text += ' '
        
            if '</author>' in line:
                author = False
            if author:
                name = line.replace('<name>', '').replace('</name>', '')
                author_list.append(name.strip())
            if '<author>' in line:
                author = True
            
        paper_dict['author'] = author_list
        paper_list.append(paper_dict)
    
    papers_df = pd.DataFrame(paper_list)
    papers_df.to_csv('data/papers.csv')
