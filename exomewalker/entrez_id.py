import mygene


def entrez_id_search(gene_symbol):

    mg = mygene.MyGeneInfo()

    gene_info = mg.query('symbol:'+gene_symbol, species='human')
    if 'hits' in gene_info:
        if len(gene_info['hits']) > 0:
            if 'entrezgene' in gene_info['hits'][0]:
                return gene_info['hits'][0]['entrezgene']

    return 'not found'

# print(entrez_id_search('cdk2'))
# print(entrez_id_search('fam83h'))
# print(entrez_id_search('jijy'))
