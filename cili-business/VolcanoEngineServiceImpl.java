package com.ruoyi.system.service.impl;

import com.ruoyi.system.domain.CiliGenerationRecord;
import com.ruoyi.system.service.IVolcanoEngineService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import com.ruoyi.common.utils.StringUtils;
import com.ruoyi.common.utils.http.HttpUtils;
import com.alibaba.fastjson2.JSON;
import com.alibaba.fastjson2.JSONObject;

import java.util.*;

/**
 * 火山引擎API服务实现
 *
 */
@Service
public class VolcanoEngineServiceImpl implements IVolcanoEngineService {

    @Value("${volcano.access-key:}")
    private String accessKey;

    @Value("${volcano.secret-key:}")
    private String secretKey;

    @Value("${volcano.endpoint:open.volcengineapi.com}")
    private String endpoint;

    @Value("${volcano.region:cn-north-1}")
    private String region;

    private static final String SERVICE_NAME = "cv";
    private static final String VERSION = "2020-08-01";

    @Override
    public String textToImage(String prompt, String negativePrompt, Map<String, Object> params) {
        String url = buildUrl("/v1/imagegen/text2img/sdxl");

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("prompt", prompt);
        if (StringUtils.isNotEmpty(negativePrompt)) {
            requestBody.put("negative_prompt", negativePrompt);
        }

        // 设置默认参数
        requestBody.putIfAbsent("style", "anime");
        requestBody.putIfAbsent("size", "1024*1024");
        requestBody.putIfAbsent("num", 1);

        // 合并自定义参数
        if (params != null) {
            requestBody.putAll(params);
        }

        try {
            String response = HttpUtils.sendPost(url, JSON.toJSONString(requestBody), getHeaders());
            JSONObject jsonResponse = JSON.parseObject(response);

            if (jsonResponse != null && jsonResponse.containsKey("task_id")) {
                return jsonResponse.getString("task_id");
            }

            throw new RuntimeException("Failed to create text2img task: " + response);
        } catch (Exception e) {
            throw new RuntimeException("Call text2img API failed: " + e.getMessage(), e);
        }
    }

    @Override
    public String imageToImage(String imageUrl, String prompt, Map<String, Object> params) {
        String url = buildUrl("/v1/imagegen/img2img");

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("image_url", imageUrl);
        requestBody.put("prompt", prompt);

        // 合并自定义参数
        if (params != null) {
            requestBody.putAll(params);
        }

        try {
            String response = HttpUtils.sendPost(url, JSON.toJSONString(requestBody), getHeaders());
            JSONObject jsonResponse = JSON.parseObject(response);

            if (jsonResponse != null && jsonResponse.containsKey("task_id")) {
                return jsonResponse.getString("task_id");
            }

            throw new RuntimeException("Failed to create img2img task: " + response);
        } catch (Exception e) {
            throw new RuntimeException("Call img2img API failed: " + e.getMessage(), e);
        }
    }

    @Override
    public String generateVideo(String imageUrl, Map<String, Object> params) {
        String url = buildUrl("/v1/videogen");

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("image_url", imageUrl);

        // 设置默认参数
        requestBody.putIfAbsent("duration", 5);
        requestBody.putIfAbsent("resolution", "720p");

        // 合并自定义参数
        if (params != null) {
            requestBody.putAll(params);
        }

        try {
            String response = HttpUtils.sendPost(url, JSON.toJSONString(requestBody), getHeaders());
            JSONObject jsonResponse = JSON.parseObject(response);

            if (jsonResponse != null && jsonResponse.containsKey("task_id")) {
                return jsonResponse.getString("task_id");
            }

            throw new RuntimeException("Failed to create video task: " + response);
        } catch (Exception e) {
            throw new RuntimeException("Call video API failed: " + e.getMessage(), e);
        }
    }

    @Override
    public Map<String, Object> queryTask(String taskId) {
        String url = buildUrl("/v1/task/query") + "?task_id=" + taskId;

        try {
            String response = HttpUtils.sendGet(url, getHeaders());
            JSONObject jsonResponse = JSON.parseObject(response);

            Map<String, Object> result = new HashMap<>();

            if (jsonResponse != null) {
                result.put("task_id", jsonResponse.getString("task_id"));
                result.put("status", jsonResponse.getString("status"));
                result.put("process_percent", jsonResponse.getInteger("process_percent"));

                // 如果任务完成，获取结果
                if ("success".equals(jsonResponse.getString("status"))) {
                    result.put("result_url", jsonResponse.getString("result_url"));
                }

                if (jsonResponse.containsKey("error")) {
                    result.put("error", jsonResponse.getString("error"));
                }
            }

            return result;
        } catch (Exception e) {
            throw new RuntimeException("Query task failed: " + e.getMessage(), e);
        }
    }

    @Override
    public String enhanceImage(String imageUrl) {
        String url = buildUrl("/v1/image/enhance");

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("image_url", imageUrl);

        try {
            String response = HttpUtils.sendPost(url, JSON.toJSONString(requestBody), getHeaders());
            JSONObject jsonResponse = JSON.parseObject(response);

            if (jsonResponse != null && jsonResponse.containsKey("task_id")) {
                return jsonResponse.getString("task_id");
            }

            throw new RuntimeException("Failed to create enhance task: " + response);
        } catch (Exception e) {
            throw new RuntimeException("Call enhance API failed: " + e.getMessage(), e);
        }
    }

    @Override
    public String inpaint(String imageUrl, String maskUrl, String prompt) {
        String url = buildUrl("/v1/image/inpaint");

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("image_url", imageUrl);
        requestBody.put("mask_url", maskUrl);
        requestBody.put("prompt", prompt);

        try {
            String response = HttpUtils.sendPost(url, JSON.toJSONString(requestBody), getHeaders());
            JSONObject jsonResponse = JSON.parseObject(response);

            if (jsonResponse != null && jsonResponse.containsKey("task_id")) {
                return jsonResponse.getString("task_id");
            }

            throw new RuntimeException("Failed to create inpaint task: " + response);
        } catch (Exception e) {
            throw new RuntimeException("Call inpaint API failed: " + e.getMessage(), e);
        }
    }

    @Override
    public String motionClone(String imageUrl, String videoUrl) {
        String url = buildUrl("/v1/video/motion_clone");

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("image_url", imageUrl);
        requestBody.put("video_url", videoUrl);

        try {
            String response = HttpUtils.sendPost(url, JSON.toJSONString(requestBody), getHeaders());
            JSONObject jsonResponse = JSON.parseObject(response);

            if (jsonResponse != null && jsonResponse.containsKey("task_id")) {
                return jsonResponse.getString("task_id");
            }

            throw new RuntimeException("Failed to create motion clone task: " + response);
        } catch (Exception e) {
            throw new RuntimeException("Call motion clone API failed: " + e.getMessage(), e);
        }
    }

    @Override
    public String digitalHuman(String imageUrl, String script) {
        String url = buildUrl("/v1/digital_human");

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("image_url", imageUrl);
        requestBody.put("script", script);

        try {
            String response = HttpUtils.sendPost(url, JSON.toJSONString(requestBody), getHeaders());
            JSONObject jsonResponse = JSON.parseObject(response);

            if (jsonResponse != null && jsonResponse.containsKey("task_id")) {
                return jsonResponse.getString("task_id");
            }

            throw new RuntimeException("Failed to create digital human task: " + response);
        } catch (Exception e) {
            throw new RuntimeException("Call digital human API failed: " + e.getMessage(), e);
        }
    }

    @Override
    public String getTaskResult(CiliGenerationRecord record) {
        if (record == null || StringUtils.isEmpty(record.getTaskId())) {
            return null;
        }

        Map<String, Object> taskResult = queryTask(record.getTaskId());
        String status = (String) taskResult.get("status");

        if ("success".equals(status)) {
            return (String) taskResult.get("result_url");
        } else if ("failed".equals(status)) {
            return (String) taskResult.get("error");
        }

        return null;
    }

    /**
     * 构建API URL
     */
    private String buildUrl(String path) {
        return "https://" + endpoint + path;
    }

    /**
     * 获取请求头
     */
    private Map<String, String> getHeaders() {
        Map<String, String> headers = new HashMap<>();
        headers.put("Content-Type", "application/json");
        headers.put("X-Date", getTimestamp());
        headers.put("X-Access-Key", accessKey);
        headers.put("X-Signature", generateSignature());
        return headers;
    }

    /**
     * 获取时间戳
     */
    private String getTimestamp() {
        return new SimpleDateFormat("yyyyMMdd'T'HHmmss'Z'").format(new Date());
    }

    /**
     * 生成签名（简化版，实际需要根据火山引擎SDK实现）
     */
    private String generateSignature() {
        // 实际实现需要使用火山引擎的签名算法
        // 这里使用简化版本
        return "";
    }
}
