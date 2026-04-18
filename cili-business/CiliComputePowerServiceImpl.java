package com.ruoyi.system.service.impl;

import java.math.BigDecimal;
import java.util.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.system.mapper.CiliComputePowerMapper;
import com.ruoyi.system.domain.CiliComputePower;
import com.ruoyi.system.service.ICiliComputePowerService;

/**
 * 用户算力Service业务层处理
 *
 */
@Service
public class CiliComputePowerServiceImpl implements ICiliComputePowerService {

    @Autowired
    private CiliComputePowerMapper ciliComputePowerMapper;

    @Override
    public CiliComputePower selectCiliComputePowerById(Long id) {
        return ciliComputePowerMapper.selectCiliComputePowerById(id);
    }

    @Override
    public CiliComputePower selectCiliComputePowerByUserId(Long userId) {
        return ciliComputePowerMapper.selectCiliComputePowerByUserId(userId);
    }

    @Override
    public List<CiliComputePower> selectCiliComputePowerList(CiliComputePower ciliComputePower) {
        return ciliComputePowerMapper.selectCiliComputePowerList(ciliComputePower);
    }

    @Override
    public int insertCiliComputePower(CiliComputePower ciliComputePower) {
        ciliComputePower.setCreateTime(new Date());
        ciliComputePower.setBalance(BigDecimal.ZERO);
        ciliComputePower.setTotalRecharged(BigDecimal.ZERO);
        ciliComputePower.setTotalUsed(BigDecimal.ZERO);
        return ciliComputePowerMapper.insertCiliComputePower(ciliComputePower);
    }

    @Override
    public int updateCiliComputePower(CiliComputePower ciliComputePower) {
        ciliComputePower.setUpdateTime(new Date());
        return ciliComputePowerMapper.updateCiliComputePower(ciliComputePower);
    }

    @Override
    public Map<String, Object> rechargePower(Long userId, BigDecimal amount) {
        Map<String, Object> result = new HashMap<>();

        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            result.put("success", false);
            result.put("message", "充值金额必须大于0");
            return result;
        }

        // 检查用户是否有算力账户
        CiliComputePower power = ciliComputePowerMapper.selectCiliComputePowerByUserId(userId);
        if (power == null) {
            // 创建新账户
            power = new CiliComputePower();
            power.setUserId(userId);
            power.setBalance(amount);
            power.setTotalRecharged(amount);
            power.setTotalUsed(BigDecimal.ZERO);
            ciliComputePowerMapper.insertCiliComputePower(power);
        } else {
            // 更新余额
            int rows = ciliComputePowerMapper.rechargePower(userId, amount);
            if (rows == 0) {
                result.put("success", false);
                result.put("message", "充值失败");
                return result;
            }
        }

        result.put("success", true);
        result.put("message", "充值成功");
        result.put("amount", amount);

        // 获取最新余额
        power = ciliComputePowerMapper.selectCiliComputePowerByUserId(userId);
        result.put("balance", power.getBalance());

        return result;
    }

    @Override
    public Map<String, Object> consumePower(Long userId, BigDecimal amount) {
        Map<String, Object> result = new HashMap<>();

        if (amount == null || amount.compareTo(BigDecimal.ZERO) <= 0) {
            result.put("success", false);
            result.put("message", "消费金额必须大于0");
            return result;
        }

        // 检查余额
        CiliComputePower power = ciliComputePowerMapper.selectCiliComputePowerByUserId(userId);
        if (power == null || !power.hasEnoughBalance(amount)) {
            result.put("success", false);
            result.put("message", "算力余额不足");
            return result;
        }

        // 扣除算力
        int rows = ciliComputePowerMapper.consumePower(userId, amount);
        if (rows == 0) {
            result.put("success", false);
            result.put("message", "消费失败，余额可能不足");
            return result;
        }

        result.put("success", true);
        result.put("message", "消费成功");
        result.put("amount", amount);

        // 获取最新余额
        power = ciliComputePowerMapper.selectCiliComputePowerByUserId(userId);
        result.put("balance", power.getBalance());

        return result;
    }

    @Override
    public boolean checkBalance(Long userId, BigDecimal amount) {
        CiliComputePower power = ciliComputePowerMapper.selectCiliComputePowerByUserId(userId);
        return power != null && power.hasEnoughBalance(amount);
    }

    @Override
    public int deleteCiliComputePowerById(Long id) {
        return ciliComputePowerMapper.deleteCiliComputePowerById(id);
    }

    @Override
    public int deleteCiliComputePowerByIds(Long[] ids) {
        return ciliComputePowerMapper.deleteCiliComputePowerByIds(ids);
    }
}
