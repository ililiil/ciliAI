package com.ruoyi.system.service;

import com.ruoyi.system.domain.CiliGenerationRecord;
import java.util.Map;

/**
 * 火山引擎API服务接口
 *
 */
public interface IVolcanoEngineService {

    /**
     * 文生图
     *
     * @param prompt 正向提示词
     * @param negativePrompt 负向提示词
     * @param params 其他参数
     * @return 任务ID
     */
    public String textToImage(String prompt, String negativePrompt, Map<String, Object> params);

    /**
     * 图生图
     *
     * @param imageUrl 参考图片URL
     * @param prompt 正向提示词
     * @param params 其他参数
     * @return 任务ID
     */
    public String imageToImage(String imageUrl, String prompt, Map<String, Object> params);

    /**
     * 视频生成
     *
     * @param imageUrl 图片URL
     * @param params 其他参数
     * @return 任务ID
     */
    public String generateVideo(String imageUrl, Map<String, Object> params);

    /**
     * 查询任务状态
     *
     * @param taskId 任务ID
     * @return 任务状态信息
     */
    public Map<String, Object> queryTask(String taskId);

    /**
     * 智能超清
     *
     * @param imageUrl 图片URL
     * @return 任务ID
     */
    public String enhanceImage(String imageUrl);

    /**
     * 局部重绘
     *
     * @param imageUrl 图片URL
     * @param maskUrl 蒙版URL
     * @param prompt 提示词
     * @return 任务ID
     */
    public String inpaint(String imageUrl, String maskUrl, String prompt);

    /**
     * 动作模仿
     *
     * @param imageUrl 人物图片URL
     * @param videoUrl 动作视频URL
     * @return 任务ID
     */
    public String motionClone(String imageUrl, String videoUrl);

    /**
     * 数字人
     *
     * @param imageUrl 数字人图片URL
     * @param script 台词脚本
     * @return 任务ID
     */
    public String digitalHuman(String imageUrl, String script);

    /**
     * 获取任务结果
     *
     * @param record 生成记录
     * @return 结果URL
     */
    public String getTaskResult(CiliGenerationRecord record);
}
