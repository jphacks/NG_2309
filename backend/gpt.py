import openai


def evaluation_score(score):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "���Ȃ��̓v���O���}�[��G���W�j�A�ɑ΂��ĐS�̌��N�����コ����悤�ȃv���̐S���J�E���Z���[�ł��Bscore�̓X�g���X���x����0���Œ�100���ō��ŃX�g���X���x����������΍����قǊ댯�ȏ�Ԃł��B�v���̃v���O���}�[�ɑ΂��Ď��̍�ƂɋC�����悭���|�����悤��50�������炢�̌��t�̃R�����g�����������܂��ȉ��̈ꕶ�͂��Ȃ��̏o�̗͂�ł��̌`���ȊO�͋����܂���B�����b�N�X���A���M�������Ď��̃v���W�F�N�g�Ɏ��g�݂܂��傤�B���N�ȐS���N���G�C�e�B�r�e�B���x���܂��B"},
        ]
    )
    return response['choices'][0]['message']['content']