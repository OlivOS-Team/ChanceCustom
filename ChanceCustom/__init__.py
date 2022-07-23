'''
_________ ___________________ ____  __.
\_   ___ \\_   ___ \______   \    |/ _|
/    \  \//    \  \/|     ___/      <  
\     \___\     \___|    |   |    |  \ 
 \______  /\______  /____|   |____|__ \
        \/        \/                 \/
@File      :   __init__.py
@Author    :   lunzhiPenxil仑质
@Contact   :   lunzhipenxil@gmail.com
@License   :   AGPL
@Copyright :   (C) 2020-2022, OlivOS-Team
@Desc      :   None
'''

import platform
from . import main
from . import load
from . import replyCore
from . import replyBase
from . import replyIO
from . import replyWeb
from . import replyRandom
from . import replyOlivaDice
from . import replyReg
if(platform.system() == 'Windows'):
    from . import GUI
