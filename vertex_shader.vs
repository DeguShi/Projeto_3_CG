attribute vec3 position;
attribute vec2 texture_coord;
attribute vec3 normals;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrix;
uniform float uv_scale;

varying vec2 out_texture;
varying vec3 out_fragPos;
varying vec3 out_normal;
varying vec4 out_lightSpacePos;

void main() {
    vec4 worldPos = model * vec4(position, 1.0);
    gl_Position   = projection * view * worldPos;
    out_texture   = texture_coord * uv_scale;
    out_fragPos   = vec3(worldPos);
    out_normal    = mat3(vec3(model[0]), vec3(model[1]), vec3(model[2])) * normals;
    out_lightSpacePos = lightSpaceMatrix * worldPos;
}
