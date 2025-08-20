"""
Analyzes extracted API details and generates documentation
"""

import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class APIPattern:
    """Represents a detected API pattern"""
    pattern_type: str
    confidence: float
    examples: List[str]
    description: str

class APIAnalyzer:
    """Analyzes extracted API details and generates documentation"""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, APIPattern]:
        """Initialize common API patterns"""
        return {
            "rest_api": APIPattern(
                pattern_type="REST API",
                confidence=0.9,
                examples=["/api/users", "/api/v1/products"],
                description="Standard REST API endpoints"
            ),
            "graphql": APIPattern(
                pattern_type="GraphQL",
                confidence=0.8,
                examples=["/graphql", "/api/graphql"],
                description="GraphQL API endpoints"
            ),
            "oauth": APIPattern(
                pattern_type="OAuth",
                confidence=0.7,
                examples=["/oauth/authorize", "/oauth/token"],
                description="OAuth authentication endpoints"
            ),
            "webhook": APIPattern(
                pattern_type="Webhook",
                confidence=0.6,
                examples=["/webhook", "/callback"],
                description="Webhook or callback endpoints"
            )
        }
    
    def analyze_patterns(self, extraction_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the extracted results for common patterns"""
        analysis = {
            "summary": {},
            "patterns": [],
            "recommendations": [],
            "security_concerns": []
        }
        
        # Analyze endpoints
        if extraction_results.get("endpoints"):
            endpoint_analysis = self._analyze_endpoints(extraction_results["endpoints"])
            analysis["summary"]["endpoints"] = endpoint_analysis
        
        # Analyze forms
        if extraction_results.get("forms"):
            form_analysis = self._analyze_forms(extraction_results["forms"])
            analysis["summary"]["forms"] = form_analysis
        
        # Analyze JavaScript
        if extraction_results.get("javascript"):
            js_analysis = self._analyze_javascript(extraction_results["javascript"])
            analysis["summary"]["javascript"] = js_analysis
        
        # Detect patterns
        detected_patterns = self._detect_patterns(extraction_results)
        analysis["patterns"] = detected_patterns
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(extraction_results)
        
        # Check for security concerns
        analysis["security_concerns"] = self._check_security_concerns(extraction_results)
        
        return analysis
    
    def _analyze_endpoints(self, endpoints: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze API endpoints"""
        analysis = {
            "total_count": len(endpoints),
            "methods": {},
            "url_patterns": [],
            "parameter_types": {}
        }
        
        for endpoint in endpoints:
            # Count HTTP methods
            method = endpoint.get("method", "GET")
            analysis["methods"][method] = analysis["methods"].get(method, 0) + 1
            
            # Analyze URL patterns
            url = endpoint.get("url", "")
            if url:
                pattern = self._extract_url_pattern(url)
                if pattern not in analysis["url_patterns"]:
                    analysis["url_patterns"].append(pattern)
            
            # Analyze parameters
            params = endpoint.get("parameters", {})
            for param_name, param_value in params.items():
                param_type = type(param_value).__name__
                if param_type not in analysis["parameter_types"]:
                    analysis["parameter_types"][param_type] = []
                analysis["parameter_types"][param_type].append(param_name)
        
        return analysis
    
    def _analyze_forms(self, forms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze form data"""
        analysis = {
            "total_count": len(forms),
            "methods": {},
            "input_types": {},
            "common_fields": []
        }
        
        field_counts = {}
        
        for form in forms:
            # Count HTTP methods
            method = form.get("method", "GET")
            analysis["methods"][method] = analysis["methods"].get(method, 0) + 1
            
            # Analyze input types
            for input_field in form.get("inputs", []):
                input_type = input_field.get("type", "text")
                analysis["input_types"][input_type] = analysis["input_types"].get(input_type, 0) + 1
                
                # Count common fields
                field_name = input_field.get("name", "")
                if field_name:
                    field_counts[field_name] = field_counts.get(field_name, 0) + 1
        
        # Get most common fields
        sorted_fields = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)
        analysis["common_fields"] = [field for field, count in sorted_fields[:10]]
        
        return analysis
    
    def _analyze_javascript(self, javascript: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze JavaScript API calls"""
        analysis = {
            "total_count": len(javascript),
            "call_types": {},
            "urls": []
        }
        
        for js in javascript:
            call_type = js.get("type", "unknown")
            analysis["call_types"][call_type] = analysis["call_types"].get(call_type, 0) + 1
            
            url = js.get("url", "")
            if url and url not in analysis["urls"]:
                analysis["urls"].append(url)
        
        return analysis
    
    def _extract_url_pattern(self, url: str) -> str:
        """Extract a pattern from a URL"""
        # Replace numbers and IDs with placeholders
        pattern = re.sub(r'/\d+', '/{id}', url)
        pattern = re.sub(r'/[a-f0-9]{8,}', '/{hash}', pattern)
        pattern = re.sub(r'/[a-zA-Z0-9]{20,}', '/{token}', pattern)
        
        return pattern
    
    def _detect_patterns(self, extraction_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect common API patterns"""
        detected = []
        
        # Check for REST API patterns
        if extraction_results.get("endpoints"):
            rest_endpoints = [ep for ep in extraction_results["endpoints"] 
                            if any(pattern in ep.get("url", "").lower() 
                                  for pattern in ["/api/", "/rest/", "/v1/", "/v2/"])]
            
            if rest_endpoints:
                detected.append({
                    "type": "REST API",
                    "confidence": 0.9,
                    "evidence": [ep["url"] for ep in rest_endpoints[:5]],
                    "description": "Multiple REST API endpoints detected"
                })
        
        # Check for GraphQL
        if extraction_results.get("endpoints"):
            graphql_endpoints = [ep for ep in extraction_results["endpoints"] 
                               if "graphql" in ep.get("url", "").lower()]
            
            if graphql_endpoints:
                detected.append({
                    "type": "GraphQL",
                    "confidence": 0.8,
                    "evidence": [ep["url"] for ep in graphql_endpoints],
                    "description": "GraphQL endpoint detected"
                })
        
        # Check for OAuth
        if extraction_results.get("endpoints"):
            oauth_endpoints = [ep for ep in extraction_results["endpoints"] 
                             if "oauth" in ep.get("url", "").lower()]
            
            if oauth_endpoints:
                detected.append({
                    "type": "OAuth",
                    "confidence": 0.7,
                    "evidence": [ep["url"] for ep in oauth_endpoints],
                    "description": "OAuth authentication endpoints detected"
                })
        
        return detected
    
    def _generate_recommendations(self, extraction_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Check for missing authentication
        if extraction_results.get("endpoints") and not extraction_results.get("api_keys"):
            recommendations.append("Consider implementing authentication for API endpoints")
        
        # Check for mixed HTTP methods
        if extraction_results.get("forms"):
            methods = set(form.get("method", "GET") for form in extraction_results["forms"])
            if len(methods) > 1:
                recommendations.append("Standardize HTTP methods across forms for consistency")
        
        # Check for API documentation
        if extraction_results.get("endpoints") and len(extraction_results["endpoints"]) > 5:
            recommendations.append("Consider adding API documentation (OpenAPI/Swagger)")
        
        return recommendations
    
    def _check_security_concerns(self, extraction_results: Dict[str, Any]) -> List[str]:
        """Check for potential security concerns"""
        concerns = []
        
        # Check for exposed API keys
        if extraction_results.get("api_keys"):
            concerns.append("API keys found in client-side code - potential security risk")
        
        # Check for sensitive data in URLs
        if extraction_results.get("endpoints"):
            sensitive_patterns = ["password", "token", "key", "secret"]
            for endpoint in extraction_results["endpoints"]:
                url = endpoint.get("url", "").lower()
                if any(pattern in url for pattern in sensitive_patterns):
                    concerns.append(f"Sensitive data in URL: {endpoint['url']}")
        
        # Check for form security
        if extraction_results.get("forms"):
            for form in extraction_results["forms"]:
                if form.get("method", "GET") == "GET":
                    concerns.append("Form using GET method may expose data in URL")
        
        return concerns
    
    def generate_api_documentation(self, extraction_results: Dict[str, Any]) -> str:
        """Generate API documentation from extracted results"""
        doc_lines = []
        
        doc_lines.append("# API Documentation")
        doc_lines.append("Generated from extracted API details")
        doc_lines.append("")
        
        # Endpoints section
        if extraction_results.get("endpoints"):
            doc_lines.append("## API Endpoints")
            doc_lines.append("")
            
            for endpoint in extraction_results["endpoints"]:
                doc_lines.append(f"### {endpoint.get('method', 'GET')} {endpoint.get('url', 'N/A')}")
                doc_lines.append("")
                
                if endpoint.get("description"):
                    doc_lines.append(f"**Description:** {endpoint['description']}")
                    doc_lines.append("")
                
                if endpoint.get("parameters"):
                    doc_lines.append("**Parameters:**")
                    for param_name, param_value in endpoint["parameters"].items():
                        doc_lines.append(f"- `{param_name}`: {param_value}")
                    doc_lines.append("")
                
                doc_lines.append("---")
                doc_lines.append("")
        
        # Forms section
        if extraction_results.get("forms"):
            doc_lines.append("## Forms")
            doc_lines.append("")
            
            for form in extraction_results["forms"]:
                doc_lines.append(f"### {form.get('method', 'GET')} {form.get('action', 'N/A')}")
                doc_lines.append("")
                
                if form.get("inputs"):
                    doc_lines.append("**Input Fields:**")
                    for input_field in form["inputs"]:
                        field_type = input_field.get("type", "text")
                        field_name = input_field.get("name", "unnamed")
                        required = " (required)" if input_field.get("required") else ""
                        doc_lines.append(f"- `{field_name}`: {field_type}{required}")
                    doc_lines.append("")
                
                doc_lines.append("---")
                doc_lines.append("")
        
        return "\n".join(doc_lines)
