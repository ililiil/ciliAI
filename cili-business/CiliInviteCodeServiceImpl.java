package com.ruoyi.system.service.impl;

import java.text.SimpleDateFormat;
import java.util.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.system.mapper.CiliInviteCodeMapper;
import com.ruoyi.system.domain.CiliInviteCode;
import com.ruoyi.system.service.ICiliInviteCodeService;
import com.ruoyi.common.utils.StringUtils;

/**
 * 邀请码Service业务层处理
 *
 */
@Service
public class CiliInviteCodeServiceImpl implements ICiliInviteCodeService {

    @Autowired
    private CiliInviteCodeMapper ciliInviteCodeMapper;

    /**
     * 查询邀请码
     *
     * @param id ID
     * @return 邀请码
     */
    @Override
    public CiliInviteCode selectCiliInviteCodeById(Long id) {
        return ciliInviteCodeMapper.selectCiliInviteCodeById(id);
    }

    /**
     * 根据邀请码查询
     *
     * @param code 邀请码
     * @return 邀请码
     */
    @Override
    public CiliInviteCode selectCiliInviteCodeByCode(String code) {
        return ciliInviteCodeMapper.selectCiliInviteCodeByCode(code);
    }

    /**
     * 查询邀请码列表
     *
     * @param ciliInviteCode 邀请码
     * @return 邀请码
     */
    @Override
    public List<CiliInviteCode> selectCiliInviteCodeList(CiliInviteCode ciliInviteCode) {
        return ciliInviteCodeMapper.selectCiliInviteCodeList(ciliInviteCode);
    }

    /**
     * 新增邀请码
     *
     * @param ciliInviteCode 邀请码
     * @return 结果
     */
    @Override
    public int insertCiliInviteCode(CiliInviteCode ciliInviteCode) {
        ciliInviteCode.setCreateTime(new Date());
        ciliInviteCode.setUsed(0);
        ciliInviteCode.setUseCount(0);
        ciliInviteCode.setStatus("0");
        return ciliInviteCodeMapper.insertCiliInviteCode(ciliInviteCode);
    }

    /**
     * 修改邀请码
     *
     * @param ciliInviteCode 邀请码
     * @return 结果
     */
    @Override
    public int updateCiliInviteCode(CiliInviteCode ciliInviteCode) {
        ciliInviteCode.setUpdateTime(new Date());
        return ciliInviteCodeMapper.updateCiliInviteCode(ciliInviteCode);
    }

    /**
     * 删除邀请码
     *
     * @param id ID
     * @return 结果
     */
    @Override
    public int deleteCiliInviteCodeById(Long id) {
        return ciliInviteCodeMapper.deleteCiliInviteCodeById(id);
    }

    /**
     * 批量删除邀请码
     *
     * @param ids 需要删除的ID
     * @return 结果
     */
    @Override
    public int deleteCiliInviteCodeByIds(Long[] ids) {
        return ciliInviteCodeMapper.deleteCiliInviteCodeByIds(ids);
    }

    /**
     * 使用邀请码
     *
     * @param code 邀请码
     * @param userId 用户ID
     * @return 结果
     */
    @Override
    public Map<String, Object> useInviteCode(String code, Long userId) {
        Map<String, Object> result = new HashMap<>();

        if (StringUtils.isEmpty(code)) {
            result.put("success", false);
            result.put("message", "邀请码不能为空");
            return result;
        }

        CiliInviteCode inviteCode = ciliInviteCodeMapper.selectCiliInviteCodeByCode(code);
        if (inviteCode == null) {
            result.put("success", false);
            result.put("message", "邀请码不存在");
            return result;
        }

        if (!inviteCode.isValid()) {
            if ("1".equals(inviteCode.getStatus())) {
                result.put("success", false);
                result.put("message", "邀请码已被禁用");
            } else if (inviteCode.getExpiresAt() != null &&
                       inviteCode.getExpiresAt().before(new Date())) {
                result.put("success", false);
                result.put("message", "邀请码已过期");
            } else {
                result.put("success", false);
                result.put("message", "邀请码已达到使用次数上限");
            }
            return result;
        }

        int rows = ciliInviteCodeMapper.useInviteCode(inviteCode.getId(), userId);
        if (rows > 0) {
            result.put("success", true);
            result.put("message", "邀请码使用成功");
            result.put("remainingUses", inviteCode.getMaxUses() - inviteCode.getUseCount() - 1);
        } else {
            result.put("success", false);
            result.put("message", "邀请码使用失败，请重试");
        }

        return result;
    }

    /**
     * 批量生成邀请码
     *
     * @param count 数量
     * @param createdBy 创建者ID
     * @param expiresAt 过期时间
     * @param maxUses 最大使用次数
     * @param batchNo 批次号
     * @return 生成的邀请码列表
     */
    @Override
    public List<String> batchGenerateInviteCodes(int count, Long createdBy,
                                                  String expiresAt, int maxUses, String batchNo) {
        List<String> codes = new ArrayList<>();

        try {
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            Date expiresDate = sdf.parse(expiresAt);

            for (int i = 0; i < count; i++) {
                CiliInviteCode inviteCode = new CiliInviteCode();
                inviteCode.setCode(generateCode());
                inviteCode.setCreatedBy(createdBy);
                inviteCode.setExpiresAt(expiresDate);
                inviteCode.setMaxUses(maxUses);
                inviteCode.setBatchNo(batchNo);

                ciliInviteCodeMapper.insertCiliInviteCode(inviteCode);
                codes.add(inviteCode.getCode());
            }
        } catch (Exception e) {
            throw new RuntimeException("生成邀请码失败：" + e.getMessage());
        }

        return codes;
    }

    /**
     * 生成邀请码
     * 格式：CILI + 年月日 + 6位随机数
     */
    private String generateCode() {
        String dateStr = new SimpleDateFormat("yyyyMMdd").format(new Date());
        String randomStr = String.format("%06d", new Random().nextInt(999999));
        return "CILI" + dateStr + randomStr;
    }
}
