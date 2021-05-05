#shader vertex
#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

out vec3 FragPos;
out vec3 Normal;

uniform mat4 uProjection;
uniform mat4 uView;
uniform mat4 uModel;

void main()
{

  FragPos = vec3(uModel * vec4(position, 1.0));
  Normal = mat3(transpose(inverse(uModel))) * normal;

  gl_Position = vec4(FragPos, 1.0) * uView * uProjection;
}

#shader fragment
#version 330 core

layout(location = 0) out vec4 color;

in vec3 FragPos;
in vec3 Normal;

uniform vec3 uColor;
vec3 lightColor = vec3(1.0, 1.0, 1.0);
vec3 lightPos = vec3(1.0, 1.0, 1.0);
float ambientStrength = 0.1;

void main()
{

  vec3 norm = normalize(Normal);
  vec3 lightDir = normalize(lightPos - FragPos);
  float diff = max(dot(norm, lightDir), 0.0);

  vec3 ambient = ambientStrength * lightColor;
  vec3 diffuse = diff * lightColor;
  vec3 result = (ambient + diffuse) * uColor;
  color = vec4(result, 1.0);
}