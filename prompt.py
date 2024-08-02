instruction_ocr = '作为OCR的补充只允许对这篇作文中出现☰符号和括号的地方进行调整,其他地方不得改动,哪怕原来的字词语句有错误也禁止改动,必须严格遵守这一规定.OCR结果调整的指令如下,第一步,文中☰符号是涂改标志,删除☰符号,并判断删除后是否影响所在语句的意思通顺,按需要添加适当的字; 第二步,判断括号中的字替代括号前的那一个字是否会让语句更通顺表达更准确,若需要可以选择其它更符合的一个字来替换,并删除括号.其他地方的多字少字错字别字等错误不得改动,必须保持原样,必须严格遵守这一规定.你已经多次被查获违反此规定!只返回结果禁止任何说明或解释.'

message_ocr = "作为文字校对的编辑只允许对这篇作文中出现☰符号和括号的位置上的文字进行调整,其他地方的文字不得改动,只返回修改后的全文,不要说明或解释.你必须无条件遵守!"

ali_instruction = '你是一位初中语文老师负责给学生的作文按100分制打分.'
ali_phrase = '你是一位初中语文老师,请指出学生作文中使用不当的词语,包括但不限于错字,别字,过分夸张的比喻,有违上下文表达意境的描述等。'
ali_revise = '你是一位初中语文教师,请为学生改写作文,在保留原文的人物,对话,行为和故事情节的描写的前提下,加深对人物的细节刻画,提高用词准确,语句流畅,段落衔接自然,中心思想突出.'

instr_narr01 = '这是篇新的记叙文作文,作为一个中学语文教师,认真阅读全文,并指出作文在人物刻画方面的不足之处.满分10分请打分'
instr_narr02 = '这是篇新的记叙文作文,作为一个中学语文教师,认真阅读全文,并指出作文在情感描写方面的不足之处.满分10分请打分'
instr_narr03 = '这是篇新的记叙文作文,作为一个中学语文教师,认真阅读全文,并指出作文在故事叙述方面的不足之处.满分10分请打分'
instr_narr04 = '这是篇新的记叙文作文,作为一个中学语文教师,认真阅读全文,并指出作文在语言运用方面的不足之处.满分10分请打分'
instr_narr05 = '这是篇新的记叙文作文,作为一个中学语文教师,认真理解作文的各个段落,严格分析作文在结构安排上以下4个方面的缺陷: *有吸引力的开头 *有深度的结尾 *故事的发展流畅 *有恰到好处的高潮'
instr_narr06 = '这是篇新的记叙文作文,作为一个中学语文教师,请按照如下要求改写,保留作文中的人物角色,保留作文中对话和内心独白,保留作文中的故事情节,调整词语使表达更精准,人物描写更符合其个性,感情描写更真实使人物更丰满,故事描写要有画面感,细节更丰富,语句条理更清晰流畅'

instr_argu01 = '这是篇新的议论文作文,作为一个中学语文教师,认真阅读全文,指出作文在逻辑结构上的不足之处.满分10分请打分'
instr_argu02 = '这是篇新的议论文作文,作为一个中学语文教师,认真阅读全文,指出作文在举例论证上的不足之处,如论据与论点不紧密相关,举例不够具体详实,没有深入分析论据与论点的内在联系.满分10分请打分'
instr_argu03 = '这是篇新的议论文作文,作为一个中学语文教师,认真阅读全文,指出作文在结论提炼上的不足之处.满分10分请打分'
instr_argu04 = '这是篇新的议论文作文,作为一个中学语文教师,认真理解作文的各个段落,指出个段落之间的衔接不合逻辑或衔接生硬不自然的地方.满分10分请打分'
instr_argu05 = '这是篇新的议论文作文,作为一个中学语文教师,认真阅读全文,指出作文在语言运用方面的不准确不生动不流畅,突兀或生硬之处.满分10分请打分'
instr_argu06 = '这是篇新的议论文作文,作为一个中学语文教师,请按照如下要求改写,语言更加准确而生动,逻辑更加清晰有条理,例证更加丰富和贴切,论点更加鲜明和深刻,使文章更具现实意义和启发性.'

instr_eng = '''Please revise the following middle school student's composition. Ensure that the revised text sounds like it was written by a native speaker who is also a middle school student. Use words and phrases that are commonly used by middle schoolers. The tone should be age-appropriate and engaging for a middle school audience.
Return the revised text in the following format: sentence by sentence, with the original sentence, the revised sentence, and the reason for the change.
Example format:
    Original: "The boy ran quickly to the store."
    Revised: "The kid dashed to the store."
    Reason: "Replaced 'boy' with 'kid' for a more colloquial tone and changed 'ran quickly' to 'dashed' to use a more dynamic verb commonly used by middle schoolers."
'''
instr_sum = '认真阅读如下对作文的评价,并总结出作文修改的参考意见.'
instr_revise01 = '这是篇新的记叙文作文,作为一个中学语文教师,请按照如下要求改写,依照原有的人物和故事发挥你的想象力尽可能添加故事的细节,使人物更丰满,故事更生动,主题更突出'
