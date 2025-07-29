import aiddit.api.unit_test.gemini_agent as gemini_agent
import aiddit.api.unit_test.tools as tools
import aiddit.utils as utils
import aiddit.model.google_genai as google_genai

if __name__ == "__main__":
    ts = []

    system_prompt = utils.read_file_as_string("/Users/nieqi/Documents/workspace/python/image_article_comprehension/aiddit/api/unit_test/agent_application/prompt/creation_persona_agent.md")
    user_input = """
账号https://www.xiaohongshu.com/user/profile/67b1fb00000000000a03c509?xsec_token=ABK82WB2Bp9l2H9W9goy8mUEz1hG7S6TECJUGg0Ik-qTs=&xsec_source=pc_feed，帮我做新的通勤穿搭内容
"""

    ans = gemini_agent.run(user_input=user_input, tools=ts, system_instruction=system_prompt,model=google_genai.MODEL_GEMINI_2_5_PRO_EXPT_0605)

    for part in ans[-1]:
        print(part.text)
