package com.ruoyi.system.service.impl;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.ruoyi.common.exception.ServiceException;
import com.ruoyi.system.mapper.CiliOrdersMapper;
import com.ruoyi.system.mapper.CiliComputePowerMapper;
import com.ruoyi.system.domain.CiliOrders;
import com.ruoyi.system.domain.CiliComputePower;
import com.ruoyi.system.service.ICiliOrdersService;

/**
 * 订单管理Service业务层处理
 *
 */
@Service
public class CiliOrdersServiceImpl implements ICiliOrdersService {

    @Autowired
    private CiliOrdersMapper ciliOrdersMapper;

    @Autowired
    private CiliComputePowerMapper ciliComputePowerMapper;

    /**
     * 查询订单管理
     *
     * @param id 订单管理主键
     * @return 订单管理
     */
    @Override
    public CiliOrders selectCiliOrdersById(Long id) {
        return ciliOrdersMapper.selectCiliOrdersById(id);
    }

    /**
     * 查询订单管理列表
     *
     * @param ciliOrders 订单管理
     * @return 订单管理
     */
    @Override
    public List<CiliOrders> selectCiliOrdersList(CiliOrders ciliOrders) {
        return ciliOrdersMapper.selectCiliOrdersList(ciliOrders);
    }

    /**
     * 新增订单管理
     *
     * @param ciliOrders 订单管理
     * @return 结果
     */
    @Override
    public int insertCiliOrders(CiliOrders ciliOrders) {
        ciliOrders.setCreateTime(new Date());
        return ciliOrdersMapper.insertCiliOrders(ciliOrders);
    }

    /**
     * 修改订单管理
     *
     * @param ciliOrders 订单管理
     * @return 结果
     */
    @Override
    public int updateCiliOrders(CiliOrders ciliOrders) {
        ciliOrders.setUpdateTime(new Date());
        return ciliOrdersMapper.updateCiliOrders(ciliOrders);
    }

    /**
     * 修改订单状态
     *
     * @param id 订单ID
     * @param status 状态
     * @return 结果
     */
    @Override
    public int updateCiliOrdersStatus(Long id, String status) {
        CiliOrders order = ciliOrdersMapper.selectCiliOrdersById(id);
        if (order == null) {
            throw new ServiceException("订单不存在");
        }
        order.setStatus(status);
        order.setUpdateTime(new Date());
        return ciliOrdersMapper.updateCiliOrders(order);
    }

    /**
     * 批量删除订单管理
     *
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    @Override
    public int deleteCiliOrdersByIds(Long[] ids) {
        return ciliOrdersMapper.deleteCiliOrdersByIds(ids);
    }

    /**
     * 删除订单管理信息
     *
     * @param id 订单管理主键
     * @return 结果
     */
    @Override
    public int deleteCiliOrdersById(Long id) {
        return ciliOrdersMapper.deleteCiliOrdersById(id);
    }

    /**
     * 退款处理
     *
     * @param id 订单ID
     * @param reason 退款原因
     * @return 结果
     */
    @Override
    @Transactional
    public Map<String, Object> refundOrder(Long id, String reason) {
        Map<String, Object> result = new HashMap<>();
        CiliOrders order = ciliOrdersMapper.selectCiliOrdersById(id);
        if (order == null) {
            result.put("success", false);
            result.put("message", "订单不存在");
            return result;
        }
        if (!"paid".equals(order.getStatus())) {
            result.put("success", false);
            result.put("message", "只有已支付的订单才能退款");
            return result;
        }
        // 更新订单状态
        order.setStatus("refunded");
        order.setRefundReason(reason);
        order.setRefundTime(new Date());
        order.setUpdateTime(new Date());
        ciliOrdersMapper.updateCiliOrders(order);
        // 退还算力
        CiliComputePower power = ciliComputePowerMapper.selectCiliComputePowerByUserId(order.getUserId());
        if (power != null) {
            power.setBalance(power.getBalance() + order.getComputePower().intValue());
            power.setUpdateTime(new Date());
            ciliComputePowerMapper.updateCiliComputePower(power);
        }
        result.put("success", true);
        result.put("message", "退款成功");
        return result;
    }

    /**
     * 获取订单统计
     *
     * @return 统计数据
     */
    @Override
    public Map<String, Object> getOrderStatistics() {
        Map<String, Object> statistics = new HashMap<>();
        // TODO: 从数据库查询统计数据
        statistics.put("totalCount", 0);
        statistics.put("todayCount", 0);
        statistics.put("totalAmount", 0.0);
        statistics.put("todayAmount", 0.0);
        return statistics;
    }
}
