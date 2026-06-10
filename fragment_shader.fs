uniform sampler2D samplerTexture;
uniform int       use_texture;
uniform vec4      flat_color;

// per-frame lighting globals
uniform vec3  lightPos[3];
uniform vec3  lightColor[3];
uniform float lightIntensity[3];
uniform int   lightEnabled[3];
uniform int   lightZone[3];

uniform int   objectZone;
uniform int   ambientEnabled;
uniform float ambientStrength;
uniform float diffuseMult;
uniform float specularMult;

// per-object material
uniform float ka;
uniform float kd;
uniform float ks;
uniform float ns;

uniform vec3  viewPos;
uniform vec3  ambientColor;
uniform int   emissive;
uniform float emissiveMult;

varying vec2 out_texture;
varying vec3 out_fragPos;
varying vec3 out_normal;

void main() {
    vec4 base_color;
    if (use_texture == 1)
        base_color = texture2D(samplerTexture, out_texture);
    else
        base_color = flat_color;

    if (emissive == 1) {
        gl_FragColor = vec4(base_color.rgb * emissiveMult, base_color.a);
        return;
    }

    vec3 result = vec3(0.0);

    if (ambientEnabled == 1)
        result += ambientStrength * ka * ambientColor * base_color.rgb;

    vec3 N = normalize(out_normal);
    vec3 V = normalize(viewPos - out_fragPos);

    for (int i = 0; i < 3; i++) {
        if (lightEnabled[i] == 1 && lightZone[i] == objectZone) {
            vec3  L      = normalize(lightPos[i] - out_fragPos);
            float diff   = max(dot(N, L), 0.0);
            vec3  diffuse = diffuseMult * kd * diff
                            * lightColor[i] * lightIntensity[i] * base_color.rgb;

            vec3  R      = reflect(-L, N);
            float spec   = pow(max(dot(V, R), 0.0), ns);
            vec3  specular = specularMult * ks * spec
                             * lightColor[i] * lightIntensity[i];

            result += diffuse + specular;
        }
    }

    gl_FragColor = vec4(result, base_color.a);
}
