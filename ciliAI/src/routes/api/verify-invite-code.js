export async function POST({ request }) {
  const { inviteCode } = await request.json();
  
  // 硬编码的邀请码列表
  const validInviteCodes = [
    '11111111',
    '22222222', 
    '33333333',
    '44444444',
    '55555555',
    '66666666',
    '77777777',
    '88888888',
    '99999999',
    '00000000'
  ];
  
  // 检查邀请码是否有效
  if (!validInviteCodes.includes(inviteCode)) {
    return new Response(
      JSON.stringify({ success: false, message: '邀请码无效' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }
  
  // 模拟防暴力破解机制 - 这里可以加入频率限制逻辑
  // 例如，记录IP地址的请求频率等
  
  // 返回成功响应，包含1000000算力
  return new Response(
    JSON.stringify({ 
      success: true, 
      message: '登录成功', 
      computingPower: 1000000 
    }),
    { status: 200, headers: { 'Content-Type': 'application/json' } }
  );
}