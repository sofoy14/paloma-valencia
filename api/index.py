# Vercel API - Health check
import json
from datetime import datetime

class handler:
    def __call__(self, request):
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'status': 'ok',
                'service': 'Paloma Valencia - Monitor Electoral',
                'message': 'API funcionando. Usa /api/news para obtener noticias',
                'timestamp': datetime.now().isoformat()
            })
        }
