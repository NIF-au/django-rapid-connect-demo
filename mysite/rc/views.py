from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import django.contrib.auth as djauth
import pwgen

# The secret that you generated and used when you
# registered your Rapid Connect service.
secret = 'SECRET_CHANGE_ME'

# The authorisation URL that AAF provided.
url = 'CHANGE_ME'

# Issuer is either 'https://rapid.test.aaf.edu.au' or 'https://rapid.aaf.edu.au'
# and the audience is the URL of your site that you registered with AAF.
config = {}
config['test.aaf.edu.au'] = {
  'iss': 'https://rapid.test.aaf.edu.au',
  'aud': 'CHANGE_ME',
}

href = '<a href="' + url + '"><img src="https://rapid.aaf.edu.au/aaf_service_439x105.png" border="0"></a>'


import jwt

def root(request):
    if request.method == 'GET':
        # TODO Use a template.
        h  = '<p> To log in, click the big button: <p> <br><br> ' + href + '<br><br>'
        h += '<p> Debug: current django user: ' + str(request.user)

        h += '<p> Debug: current requests.attributes: '
        
        if 'attributes' in request.session:
            h += str(request.session['attributes'])
        else:
            h += 'NULL'

        h += '<br><br><br>'
        return HttpResponse(h)

@csrf_exempt
def auth(request):
    if request.method != 'POST': return HttpResponse('nope')

    try:
        # Verifies signature and expiry time
        verified_jwt = jwt.decode(request.POST['assertion'], secret)
     
        print 'verified_jwt:', verified_jwt

        # In a complete app we'd also store and validate the jti value to ensure there is no replay attack
        if verified_jwt['aud'] == config['test.aaf.edu.au']['aud'] and verified_jwt['iss'] == config['test.aaf.edu.au']['iss']:
            request.session['attributes'] = verified_jwt['https://aaf.edu.au/attributes']
            request.session['jwt'] = verified_jwt
            request.session['jws'] = request.POST['assertion']

            good_email = request.session['attributes']['mail']

            if not User.objects.filter(username=good_email).count():
                u = User.objects.create_superuser(good_email, good_email, pwgen.pwgen(20, 1, no_symbols=True))
            else:
                u = User.objects.get(username=good_email)

            # Temporary workaround: http://stackoverflow.com/a/23771930
            u.backend = 'django.contrib.auth.backends.ModelBackend'

            djauth.login(request, u)

            return redirect('welcome')
        else:
            # Not for this audience
            del request.session['attributes']
            djauth.logout(request)
            raise PermissionDenied
    except jwt.ExpiredSignature:
        # Security cookie has expired
        del request.session['attributes']
        djauth.logout(request)
        raise PermissionDenied

def logout(request):
    del request.session['attributes']
    djauth.logout(request)
    return redirect('root')

def welcome(request):
    if request.method != 'GET': return HttpResponse('nope')

    if 'attributes' in request.session:
        # TODO Use a template.
        h =  '<p> Success! You have been authenticated via AAF\'s Rapid Connect service! </p>'
        h += '<p> Here is everything in the session dict: </p> <br><br>'

        for (key, value) in request.session['attributes'].iteritems():
            h += '%s: %s <br>' % (key, value,)

        h += '<br><br>'

        h += '<p> Hey, you could pop over to the <a href="/admin">django admin interface</a> using your newly created AAF identity! </p>'
        h += '<p> For example, look at the <a href="/admin/auth/user/">admin/user</a> page. </p>'

        h += '<br><br>'

        h += '<a href="/rc/logout">Logout from this site</a> (your institution single-sign-on session will be active until you close your browser session). '
        return HttpResponse(h)
    else:
        return redirect('root')
