import argparse
from pyseoa.analyzer import BatchSEOAnalyzer, disallow_keyword, allow_keyword
from pyseoa.smart_batch_analyzer import SmartBatchSEOAnalyzer
from typing import List
from pyseoa.exports.exporter_factory import ExporterFactory

def main():
    parser = argparse.ArgumentParser('Run SEO Analysis on one or more URLs')
    parser.add_argument('urls', nargs='*', help='List of URLs to analyze')
    parser.add_argument('-f', '--file', help='Path to text or CSV file containing URLs')
    parser.add_argument('-o', '--out', default='seo_reports', help='Output directory')
    parser.add_argument('-w', '--workers', default=3, help='Number of threads')
    # v0.2.0
    parser.add_argument('-t', '--terminal', action='store_true', help='Prints the report(s) to the terminal')
    parser.add_argument('-g', '--googleapikey', help='Google API Key for PageSpeed Insights')
    parser.add_argument('-e', '--export', choices=['json','csv','html','fancy_html','markdown','pdf','terminal'], default='teminal', help='Export format')
    parser.add_argument('-c', '--crawl', action="store_true", help="Crawl internal links from each given URL")
    
    args = parser.parse_args()

    # Load URLs from file if provided
    urls = args.urls
    if args.file:
        with open(args.file, 'r') as f:
            urls.extend([line.strip() for line in f if line.strip()])
    
    if not urls:
        print('❗ No urls provided.')
        return
    
    # Run batch analysis
    api_key = args.googleapikey
    # v0.2.0
    analyzer_class = SmartBatchSEOAnalyzer if args.crawl else BatchSEOAnalyzer
    analyzer = analyzer_class(urls, follow_links=args.crawl, workers=args.workers, google_api_key=api_key)
    analyzer.run_batch_analysis(max_workers=args.workers)
    
    # Export resuls
    factory = ExporterFactory()
    exporter = factory.get_exporter(args.export, output_dir=args.out) if args.export != 'csv' else factory.get_exporter(args.export, output_file='seo_summary.csv')
    exporter.export(analyzer.results, analyzer.original_urls, workers=args.workers)

if __name__ == '__main__':
    main()