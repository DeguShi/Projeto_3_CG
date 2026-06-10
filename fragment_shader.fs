uniform sampler2D samplerTexture;
uniform sampler2D shadowMap;
uniform int       use_texture;
uniform vec4      flat_color;

// Iluminação da cena
uniform vec3  lightPos[4];
uniform vec3  lightColor[4];
uniform float lightIntensity[4];
uniform int   lightEnabled[4];
uniform int   lightZone[4];

uniform int   objectZone;
uniform int   ambientEnabled;
uniform float ambientStrength;
uniform float diffuseMult;
uniform float specularMult;

// Material do objeto
uniform float ka;
uniform float kd;
uniform float ks;
uniform float ns;

uniform vec3  viewPos;
uniform vec3  ambientColor;
uniform int   emissive;
uniform float emissiveMult;
uniform int   shadowEnabled;
uniform float shadowBias;
uniform vec2  shadowTexelSize;
uniform int   shadowLightIndex;
uniform int   spotEnabled;
uniform int   spotIndex;
uniform vec3  spotDirection;
uniform float spotInnerCutoff;
uniform float spotOuterCutoff;
uniform float spotRange;

varying vec2 out_texture;
varying vec3 out_fragPos;
varying vec3 out_normal;
varying vec4 out_lightSpacePos;

float shadowAmount(vec3 normal, vec3 lightDir) {
    vec3 proj = out_lightSpacePos.xyz / out_lightSpacePos.w;
    proj = proj * 0.5 + 0.5;

    if (proj.x < 0.0 || proj.x > 1.0 ||
        proj.y < 0.0 || proj.y > 1.0 ||
        proj.z < 0.0 || proj.z > 1.0)
        return 0.0;

    float bias = max(shadowBias * (1.0 - dot(normal, lightDir)), shadowBias * 0.35);
    float shadow = 0.0;
    for (int x = -1; x <= 1; x++) {
        for (int y = -1; y <= 1; y++) {
            float closest = texture2D(shadowMap, proj.xy + vec2(x, y) * shadowTexelSize).r;
            shadow += (proj.z - bias > closest) ? 1.0 : 0.0;
        }
    }
    return shadow / 9.0;
}

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

    for (int i = 0; i < 4; i++) {
        if (lightEnabled[i] == 1 &&
            (lightZone[i] == objectZone || lightZone[i] == 2 || objectZone == 2)) {
            vec3  L      = normalize(lightPos[i] - out_fragPos);
            float diff   = max(dot(N, L), 0.0);
            float factor  = 1.0;

            if (spotEnabled == 1 && i == spotIndex) {
                vec3 fragDir = normalize(out_fragPos - lightPos[i]);
                float theta = dot(fragDir, normalize(spotDirection));
                float cone = clamp((theta - spotOuterCutoff) /
                                   (spotInnerCutoff - spotOuterCutoff), 0.0, 1.0);
                float dist = length(lightPos[i] - out_fragPos);
                float range = clamp(1.0 - dist / spotRange, 0.0, 1.0);
                factor = cone * range * range;
            }

            vec3  diffuse = diffuseMult * kd * diff
                            * lightColor[i] * lightIntensity[i] * factor * base_color.rgb;

            vec3  R      = reflect(-L, N);
            float spec   = pow(max(dot(V, R), 0.0), ns);
            vec3  specular = specularMult * ks * spec
                             * lightColor[i] * lightIntensity[i] * factor;

            float visibility = 1.0;
            if (i == shadowLightIndex && shadowEnabled == 1)
                visibility = 1.0 - shadowAmount(N, L);

            result += visibility * (diffuse + specular);
        }
    }

    gl_FragColor = vec4(result, base_color.a);
}
