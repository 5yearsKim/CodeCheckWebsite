import io
from contextlib import redirect_stdout
import traceback
import timeout_decorator

@timeout_decorator.timeout(3, use_signals=False)
def check_answer(answer_code, test_expression, mode='dbg'):
    buf = io.StringIO()
    with redirect_stdout(buf):
        if "rm -rf" in answer_code or "import os" in answer_code or "from os" in answer_code:
            return "code_error", "Potential Danger Included! do not import os"
        try:
            exec(answer_code, locals())
        except:
            m_stdout = buf.getvalue()
            return "code_error", traceback.format_exc(), m_stdout
    m_stdout = buf.getvalue()
    answer = []
    # exec("answer = factorial(5) ")
    comm = "ans = "
    try:
        for i in range(len(test_expression)):
            if mode == 'dbg':
                exec(comm + test_expression[i], locals())
                exec("answer.append(ans)", locals())
            else: #mode is test mode
                try:
                    exec(comm + test_expression[i], locals())
                    exec("answer.append(ans)", locals())
                except:
                    exec("answer.append(\'error\')")
    except:
        return "test_error", traceback.format_exc(), m_stdout
    return answer, None, m_stdout

def get_score(answer, t_val, max_score):
    N_ans = min(len(answer), len(t_val))
    if N_ans == 0:
        return max_score
    hit, miss = 0, 0
    for i in range(N_ans):
        if is_number(answer[i]) and is_number(t_val[i]):
            try:
                val = float(answer[i]) / float(t_val[i])
            except ZeroDivisionError:
                val = (float(answer[i]) + 1) / (float(t_val[i]) + 1)

            if val > 0.98 and val < 1.02:
                hit += 1
            else:
                miss += 1
        else:
            if str(answer[i]) == str(t_val[i]):
                hit += 1
            else:
                miss += 1
    return round(max_score * (hit /(hit + miss)), 1)

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False



