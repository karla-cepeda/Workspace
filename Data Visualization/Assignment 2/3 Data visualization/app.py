import dash
import dash_bootstrap_components as dbc

# bootstrap theme
# https://bootswatch.com/lux/
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.LITERA],)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <!-- Cookie Consent by https://www.FreePrivacyPolicy.com -->
        <script type="text/javascript" src="//www.freeprivacypolicy.com/public/cookie-consent/3.1.0/cookie-consent.js"></script>
        <script type="text/javascript">
        document.addEventListener('DOMContentLoaded', function () {
        cookieconsent.run({"notice_banner_type":"interstitial","consent_type":"express","palette":"light","language":"en","website_name":"My Data Visualization Project","cookies_policy_url":"http://datavis.tanniestudio.com/policyprivacy.html"});
        });
        </script>
        
        <!-- Google Analytics -->
        <!-- Global site tag (gtag.js) - Google Analytics -->
                <script type="text/plain" cookie-consent="tracking" async src="https://www.googletagmanager.com/gtag/js?id=G-MYTNZCYLVW"></script>
                <script type="text/plain" cookie-consent="tracking">
                  window.dataLayer = window.dataLayer || [];
                  function gtag(){dataLayer.push(arguments);}
                  gtag('js', new Date());
                
                  gtag('config', 'G-MYTNZCYLVW');
                </script>
        <!-- end of Google Analytics-->
        
        <noscript>Cookie Consent by <a href="https://www.FreePrivacyPolicy.com/free-cookie-consent/" rel="nofollow noopener">FreePrivacyPolicy.com</a></noscript>
        <!-- End Cookie Consent -->
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.title = "Moby bikes"

server = app.server
app.config.suppress_callback_exceptions = True

