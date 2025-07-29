"""
pyseoa: Python SEO Analyzer

https://github.com/sempre76/pyseoa
"""

from .analyzer import (
    SEOAnalyzer, BatchSEOAnalyzer,
    disallow_keyword, allow_keyword, get_disallowed_keywords,
    FLAG_NONE, FLAG_TITLE, FLAG_META_DESCRIPTION, FLAG_H1_TAGS, FLAG_ALT_TAGS, FLAG_CANONICAL, FLAG_OPENGRAPH, FLAG_TWITTER, FLAG_ROBOTS_TXT, 
    FLAG_SITEMAP, FLAG_FAVICON, FLAG_KEYWORD_DENSITY, FLAG_MOBILE_FRIENDLY, FLAG_LINKS, FLAG_NOFOLLOW_LINKS, FLAG_HREFLANG, FLAG_META_ROBOTS, 
    FLAG_WEBVITALS, FLAG_ACCESSIBILIY, FLAG_STRUCTERED_DATA, FLAG_AMP_COMPLIANCE, FLAG_ALL,
)
from .smart_batch_analyzer import SmartBatchSEOAnalyzer



__all__ = [
    # classes
    "SEOAnalyzer", "BatchSEOAnalyzer", "SmartBatchSEOAnalyzer",

    # functions
    "disallow_keyword", "allow_keyword", "get_disallowed_keywords",

    # flags
    'FLAG_NONE', 'FLAG_TITLE', 'FLAG_META_DESCRIPTION', 'FLAG_H1_TAGS', 'FLAG_ALT_TAGS', 'FLAG_CANONICAL', 'FLAG_OPENGRAPH', 'FLAG_TWITTER', 'FLAG_ROBOTS_TXT', 
    'FLAG_SITEMAP', 'FLAG_FAVICON', 'FLAG_KEYWORD_DENSITY', 'FLAG_MOBILE_FRIENDLY', 'FLAG_LINKS', 'FLAG_NOFOLLOW_LINKS', 'FLAG_HREFLANG', 'FLAG_META_ROBOTS', 
    'FLAG_WEBVITALS', 'FLAG_ACCESSIBILIY', 'FLAG_STRUCTERED_DATA', 'FLAG_AMP_COMPLIANCE', 'FLAG_ALL',
]


__title__       = "pyseoa"
__description__ = "A SEO analysis toolkit written in Python, with CLI, threading, exporters, and crawler support."
__version__     = "0.2.3.post1"
__author__      = "masem"
__email__       = "contact@masem.at"
__url__         = "https://github.com/sempre76/pyseoa"
__license__     = "MIT"
__keywords__    = ["seo", "cli", "python", "crawler", "analyzer", "export"]
