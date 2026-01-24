#version 450

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec3 inColor;
layout(location = 2) in mat4 inInstanceModel;
layout(location = 6) in vec4 inInstanceColor;

layout(location = 0) out vec3 fragColor;
layout(location = 1) out vec2 fragTexCoord;

layout(binding = 0) uniform UniformBufferObject {
    mat4 model;
    mat4 view;
    mat4 proj;
} ubo;

void main() {
    mat4 modelMatrix = inInstanceModel;
    if (modelMatrix[0][0] == 0.0 && modelMatrix[0][1] == 0.0) {
        modelMatrix = ubo.model;
    }
    
    gl_Position = ubo.proj * ubo.view * modelMatrix * vec4(inPosition, 1.0);
    fragColor = inColor * inInstanceColor.rgb;
    fragTexCoord = vec2(0.0, 0.0); // Would come from vertex data
}
